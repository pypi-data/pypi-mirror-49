#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved.

from typing import Any, Dict, List, Optional, Tuple, Union

import ax.service.utils.best_point as best_point_utils
import numpy as np
from ax.core.arm import Arm
from ax.core.data import Data
from ax.core.experiment import Experiment
from ax.core.trial import Trial
from ax.core.types import (
    TEvaluationOutcome,
    TModelPredictArm,
    TParameterization,
    TParamValue,
)
from ax.modelbridge.generation_strategy import GenerationStrategy
from ax.plot.base import AxPlotConfig
from ax.plot.contour import plot_contour
from ax.plot.trace import optimization_trace_single_method
from ax.service.utils.dispatch import choose_generation_strategy
from ax.service.utils.instantiation import make_experiment
from ax.utils.common.docutils import copy_doc
from ax.utils.common.logger import get_logger
from ax.utils.common.typeutils import checked_cast, not_none, numpy_type_to_python_type


logger = get_logger(__name__)


try:  # We don't require SQLAlchemy by default.
    from ax.storage.sqa_store.structs import DBSettings
except ModuleNotFoundError:  # pragma: no cover
    DBSettings = None


class AxClient:
    """
    Convenience handler for management of experimentation cycle through a
    service-like API. External system manages scheduling of the cycle and makes
    calls to this client to get next suggestion in the experiment and log back
    data from the evaluation of that suggestion.

    Note: `AxClient` expects to only propose 1 arm (suggestion) per trial; support
    for use cases that require use of batches is coming soon.

    Two custom types used in this class for convenience are `TParamValue` and
    `TParameterization`. Those are shortcuts for `Union[str, bool, float, int]`
    and `Dict[str, Union[str, bool, float, int]]`, respectively.

    Args:
        generation_strategy: Optional generation strategy. If not set, one is
            intelligently chosen based on properties of search space.

        db_settings: Settings for saving and reloading the underlying experiment
            to a database.

        enforce_sequential_optimization: Whether to enforce that when it is
            reasonable to switch models during the optimization (as prescribed
            by `num_arms` in generation strategy), Ax will wait for enough trials
            to be completed with data to proceed. Defaults to True. If set to
            False, Ax will keep generating new trials from the previous model
            until enough data is gathered. Use this only if necessary;
            otherwise, it is more resource-efficient to
            optimize sequentially, by waiting until enough data is available to
            use the next model.
    """

    def __init__(
        self,
        generation_strategy: Optional[GenerationStrategy] = None,
        db_settings: Any = None,
        enforce_sequential_optimization: bool = True,
    ) -> None:
        self.generation_strategy = generation_strategy
        if db_settings and (not DBSettings or not isinstance(db_settings, DBSettings)):
            raise ValueError(
                "`db_settings` argument should be of type ax.storage.sqa_store."
                "structs.DBSettings. To use `DBSettings`, you will need SQLAlchemy "
                "installed in your environment (can be installed through pip)."
            )
        self.db_settings = db_settings
        self._experiment: Optional[Experiment] = None
        self._enforce_sequential_optimization = enforce_sequential_optimization
        # Trials, for which we received data since last `GenerationStrategy.gen`,
        # used to make sure that generation strategy is updated with new data.
        self._updated_trials: List[int] = []

    # ------------------------ Public API methods. ------------------------

    def create_experiment(
        self,
        parameters: List[Dict[str, Union[TParamValue, List[TParamValue]]]],
        name: Optional[str] = None,
        objective_name: Optional[str] = None,
        minimize: bool = False,
        parameter_constraints: Optional[List[str]] = None,
        outcome_constraints: Optional[List[str]] = None,
        status_quo: Optional[TParameterization] = None,
    ) -> None:
        """Create a new experiment and save it if DBSettings available.

        Args:
            parameters: List of dictionaries representing parameters in the
                experiment search space. Required elements in the dictionaries
                are: "name" (name of this parameter, string), "type" (type of the
                parameter: "range", "fixed", or "choice", string), and "bounds"
                for range parameters (list of two values, lower bound first),
                "values" for choice parameters (list of values), and "value" for
                fixed parameters (single value).
            objective: Name of the metric used as objective in this experiment.
                This metric must be present in `raw_data` argument to `complete_trial`.
            name: Name of the experiment to be created.
            minimize: Whether this experiment represents a minimization problem.
            parameter_constraints: List of string representation of parameter
                constraints, such as "x3 >= x4" or "x3 + x4 + x5 >= 2". For sum
                constraints, any number of arguments is accepted, and acceptable
                operators are "<=" and ">=".
            outcome_constraints: List of string representation of outcome
                constraints of form "metric_name >= bound", like "m1 <= 3."
            status_quo: Parameterization of the current state of the system.
                If set, this will be added to each trial to be evaluated alongside
                test configurations.
        """
        if self.db_settings and not name:
            raise ValueError(  # pragma: no cover
                "Must give the experiment a name if `db_settings` is not None."
            )

        self._experiment = make_experiment(
            name=name,
            parameters=parameters,
            objective_name=objective_name,
            minimize=minimize,
            parameter_constraints=parameter_constraints,
            outcome_constraints=outcome_constraints,
            status_quo=status_quo,
        )
        if self.generation_strategy is None:
            self.generation_strategy = choose_generation_strategy(
                search_space=self._experiment.search_space,
                enforce_sequential_optimization=self._enforce_sequential_optimization,
            )
        self._save_experiment_if_possible()

    def get_next_trial(self) -> Tuple[TParameterization, int]:
        """
        Generate trial with the next set of parameters to try in the iteration process.

        Note: Service API currently supports only 1-arm trials.

        Returns:
            Tuple of trial parameterization, trial index
        """
        # NOTE: Could move this into complete_trial to save latency on this call.
        trial = self._suggest_new_trial()
        trial.mark_dispatched()
        self._updated_trials = []
        self._save_experiment_if_possible()
        return not_none(trial.arm).parameters, trial.index

    def complete_trial(
        self,
        trial_index: int,
        # acceptable `raw_data` argument formats:
        # 1) {metric_name -> (mean, standard error)}
        # 2) (mean, standard error) and we assume metric name == objective name
        # 3) only the mean, and we assume metric name == objective name and
        #    standard error == 0
        raw_data: TEvaluationOutcome,
        metadata: Optional[Dict[str, str]] = None,
        sample_size: Optional[int] = None,
    ) -> None:
        """
        Completes the trial with given metric values and adds optional metadata
        to it.

        Args:
            trial_index: Index of trial within the experiment.
            raw_data: Evaluation data for the trial. Can be a mapping from
                metric name to a tuple of mean and SEM, just a tuple of mean and
                SEM if only one metric in optimization, or just the mean if there
                is no SEM.
            metadata: Additional metadata to track about this run.
        """
        assert isinstance(
            trial_index, int
        ), f"Trial index must be an int, got: {trial_index}."  # pragma: no cover
        trial = self.experiment.trials[trial_index]
        if not isinstance(trial, Trial):
            raise NotImplementedError(
                "Batch trial functionality is not yet available through Service API."
            )

        if metadata is not None:
            trial._run_metadata = metadata

        arm_name = not_none(trial.arm).name
        if isinstance(raw_data, dict):
            evaluations = {arm_name: raw_data}
        elif isinstance(raw_data, tuple):
            evaluations = {
                arm_name: {
                    self.experiment.optimization_config.objective.metric.name: raw_data
                }
            }
        elif isinstance(raw_data, (float, int)):
            evaluations = {
                arm_name: {
                    self.experiment.optimization_config.objective.metric.name: (
                        raw_data,
                        0.0,
                    )
                }
            }
        elif isinstance(raw_data, (np.float32, np.float64, np.int32, np.int64)):
            evaluations = {
                arm_name: {
                    self.experiment.optimization_config.objective.metric.name: (
                        numpy_type_to_python_type(raw_data),
                        0.0,
                    )
                }
            }
        else:
            raise ValueError(
                "Raw data has an invalid type. The data must either be in the form "
                "of a dictionary of metric names to mean, sem tuples, "
                "or a single mean, sem tuple, or a single mean."
            )

        sample_sizes = {arm_name: sample_size} if sample_size else {}
        data = Data.from_evaluations(evaluations, trial.index, sample_sizes)
        trial.mark_completed()
        self.experiment.attach_data(data)
        self._updated_trials.append(trial_index)
        self._save_experiment_if_possible()

    def log_trial_failure(
        self, trial_index: int, metadata: Optional[Dict[str, str]] = None
    ) -> None:
        """Mark that the given trial has failed while running.

        Args:
            trial_index: Index of trial within the experiment.
            metadata: Additional metadata to track about this run.
        """
        trial = self.experiment.trials[trial_index]
        trial.mark_failed()
        if metadata is not None:
            trial._run_metadata = metadata
        self._save_experiment_if_possible()

    def attach_trial(
        self, parameters: TParameterization
    ) -> Tuple[TParameterization, int]:
        """Attach a new trial with the given parameterization to the experiment.

        Args:
            parameters: Parameterization of the new trial.

        Returns:
            Tuple of parameterization and trial index from newly created trial.
        """
        trial = self.experiment.new_trial().add_arm(Arm(parameters=parameters))
        trial.mark_dispatched()
        self._save_experiment_if_possible()
        return not_none(trial.arm).parameters, trial.index

    @copy_doc(best_point_utils.get_best_parameters)
    def get_best_parameters(
        self
    ) -> Optional[Tuple[TParameterization, Optional[TModelPredictArm]]]:
        return best_point_utils.get_best_parameters(self.experiment)

    def get_recommended_max_parallelism(self) -> List[Tuple[int, int]]:
        """Recommends maximum number of trials that can be scheduled in parallel
        at different stages of optimization.

        Some optimization algorithms profit significantly from sequential
        optimization (e.g. suggest a few points, get updated with data for them,
        repeat). This setting indicates how many trials should be in flight
        (generated, but not yet completed with data).

        The output of this method is mapping of form
        {num_trials -> max_parallelism_setting}, where the max_parallelism_setting
        is used for num_trials trials. If max_parallelism_setting is -1, as
        many of the trials can be ran in parallel, as necessary. If num_trials
        in a tuple is -1, then the corresponding max_parallelism_setting
        should be used for all subsequent trials.

        For example, if the returned list is [(5, -1), (12, 6), (-1, 3)],
        the schedule could be: run 5 trials in parallel, run 6 trials in
        parallel twice, run 3 trials in parallel for as long as needed. Here,
        'running' a trial means obtaining a next trial from `AxClient` through
        get_next_trials and completing it with data when available.

        Returns:
            Mapping of form {num_trials -> max_parallelism_setting}.
        """
        if not (self._experiment and self.generation_strategy):
            # Auto-selected generation strategy is set on experiment creation.
            raise ValueError(
                "`get_recommended_max_parallelism` requires an experiment to be "
                "set on AxClient first."
            )
        parallelism_settings = []
        for step in self.generation_strategy._steps:
            parallelism_settings.append(
                (step.num_arms, step.recommended_max_parallelism or step.num_arms)
            )
        return parallelism_settings

    def get_optimization_trace(
        self, objective_optimum: Optional[float] = None
    ) -> AxPlotConfig:
        """Retrieves the plot configuration for optimization trace, which shows
        the evolution of the objective mean over iterations.

        Args:
            objective_optimum: Optimal objective, if known, for display in the
                visualization.
        """
        if not self.experiment.trials:
            raise ValueError("Cannot generate plot as there are no trials.")
        objective_name = self.experiment.optimization_config.objective.metric.name
        best_objectives = np.array(
            [
                [
                    checked_cast(Trial, trial).objective_mean
                    for trial in self.experiment.trials.values()
                ]
            ]
        )
        return optimization_trace_single_method(
            y=(
                np.minimum.accumulate(best_objectives, axis=1)
                if self.experiment.optimization_config.objective.minimize
                else np.maximum.accumulate(best_objectives, axis=1)
            ),
            optimum=objective_optimum,
            title="Model performance vs. # of iterations",
            ylabel=objective_name.capitalize(),
        )

    def get_contour_plot(
        self,
        param_x: Optional[str] = None,
        param_y: Optional[str] = None,
        metric_name: Optional[str] = None,
    ) -> AxPlotConfig:
        """Retrieves a plot configuration for a contour plot of the response
        surface. For response surfaces with more than two parameters,
        selected two parameters will appear on the axes, and remaining parameters
        will be affixed to the middle of their range. If contour params arguments
        are not provided, the first two parameters in the search space will be
        used. If contour metrics are not provided, objective will be used.

        Args:
            param_x: name of parameters to use on x-axis for
                the contour response surface plots.
            param_y: name of parameters to use on y-axis for
                the contour response surface plots.
            metric_name: Name of the metric, for which to plot the response
                surface.
        """
        if not self.experiment.trials:
            raise ValueError("Cannot generate plot as there are no trials.")
        assert (
            self.generation_strategy
        ), "Cannot plot response surface without generation strategy."
        if len(self.experiment.parameters) < 2:
            raise ValueError(
                "Cannot create a contour plot as experiment has less than 2 "
                "parameters, but a contour-related argument was provided."
            )
        if (param_x or param_y) and not (param_x and param_y):
            raise ValueError(
                "If `param_x` is provided, `param_y` is "
                "required as well, and vice-versa."
            )
        objective_name = self.experiment.optimization_config.objective.metric.name
        if not metric_name:
            metric_name = objective_name

        if not param_x or not param_y:
            parameter_names = list(self.experiment.parameters.keys())
            param_x = parameter_names[0]
            param_y = parameter_names[1]

        if param_x not in self.experiment.parameters:
            raise ValueError(
                f'Parameter "{param_x}" not found in the optimization search space.'
            )
        if param_y not in self.experiment.parameters:
            raise ValueError(
                f'Parameter "{param_y}" not found in the optimization search space.'
            )
        if metric_name not in self.experiment.metrics:
            raise ValueError(
                f'Metric "{metric_name}" is not associated with this optimization.'
            )
        if self.generation_strategy.model is not None:
            try:
                return plot_contour(
                    model=self.generation_strategy.model,
                    param_x=param_x,
                    param_y=param_y,
                    metric_name=metric_name,
                )
            except NotImplementedError:
                # Some models don't implement '_predict', which is needed
                # for the contour plots.
                pass
        raise ValueError(
            f'Could not obtain contour plot of "{metric_name}" for parameters '
            f'"{param_x}" and "{param_y}", as a model with predictive ability, '
            "such as a Gaussian Process, has not yet been trained in the course "
            "of this optimization."
        )

    def load_experiment(self, experiment_name: str) -> None:
        """[Work in progress] Load an existing experiment.

        Args:
            experiment_name: Name of the experiment.

        Returns:
            Experiment object.
        """
        raise NotImplementedError(  # pragma: no cover
            "Saving and loading experiment in `AxClient` functionality currently "
            "under development."
        )

    def get_report(self) -> str:
        """Returns HTML of a generated report containing vizualizations."""
        raise NotImplementedError(  # pragma: no cover
            "Report generation not supported for `AxClient` yet."
        )

    def should_stop_early(self, trial_index: int, data: TEvaluationOutcome) -> bool:
        """Whether to stop the given parameterization given early data."""
        raise NotImplementedError(  # pragma: no cover
            "Early stopping of trials not supported for `AxClient` yet."
        )

    # ---------------------- Private helper methods. ---------------------

    @property
    def experiment(self) -> Experiment:
        """Returns the experiment set on this Ax client"""
        if self._experiment is None:
            raise ValueError(
                "Experiment not set on Ax client. Must first "
                "call load_experiment or create_experiment to use handler functions."
            )
        return self._experiment

    def _save_experiment_if_possible(self) -> bool:
        """[Work in progress] Saves attached experiment if DB settings are set on this AxClient
        instance.

        Returns:
            bool: Whether the experiment was saved.
        """
        if self.db_settings and self._experiment:
            raise NotImplementedError(  # pragma: no cover
                "Saving and loading experiment in `AxClient` functionality "
                "currently under development."
            )
        return False

    def _get_new_data(self) -> Data:
        """
        Returns new data since the last run of the generator.

        Returns:
            Latest data.
        """
        return Data.from_multiple_data(
            [self.experiment.lookup_data_for_trial(idx) for idx in self._updated_trials]
        )

    def _suggest_new_trial(self) -> Trial:
        """
        Suggest new candidate for this experiment.

        Args:
            n: Number of candidates to generate.

        Returns:
            Trial with candidate.
        """
        new_data = self._get_new_data()
        generator_run = not_none(self.generation_strategy).gen(
            experiment=self.experiment, new_data=new_data
        )
        return self.experiment.new_trial(generator_run=generator_run)
