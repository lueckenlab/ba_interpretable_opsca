"""High-level entry point bundling data, annotations and analyses."""

from __future__ import annotations

import pandas as pd

from . import pl, pp, tl


class MetricExplorer:
    """Explore metric behaviour over a real or simulated search space.

    Parameters
    ----------
    scores
        Long score table (see :mod:`metricscape.io`); for simulations use
        :func:`metricscape.sim.simulate_scores`.
    metadata
        Optional per-dataset table with a ``dataset_id`` column holding covariates
        (e.g. batch imbalance). Merged into the scores. Not needed if ``scores``
        already carries the covariates (simulated spaces).
    controls, metric_types
        Optional overrides of :data:`metricscape.pp.DEFAULT_CONTROLS` and
        :data:`metricscape.pp.DEFAULT_METRIC_TYPES`.

    Examples
    --------
    >>> ex = MetricExplorer(scores, metadata)  # doctest: +SKIP
    >>> ex.response("batch_imbalance")  # doctest: +SKIP
    """

    def __init__(
        self,
        scores: pd.DataFrame,
        metadata: pd.DataFrame | None = None,
        controls: dict[str, str] | None = None,
        metric_types: dict[str, str] | None = None,
    ):
        df = scores
        if metadata is not None:
            df = df.merge(metadata, on="dataset_id", how="inner")
        df = pp.annotate_controls(df, controls)
        self.data = pp.annotate_metric_types(df, metric_types)

    def response(self, covariate: str, controls: bool = False, **kwargs) -> pd.DataFrame:
        """Per-metric, per-method linear response to ``covariate`` (see :func:`metricscape.tl.metric_response`).

        Parameters
        ----------
        controls
            Analyse control methods instead of real methods.
        """
        group = "control method" if controls else "non-control method"
        return tl.metric_response(self.data[self.data["control_group"] == group], covariate, **kwargs)

    def correlation(self, **kwargs) -> pd.DataFrame:
        """Metric correlation across runs (see :func:`metricscape.tl.metric_correlation`)."""
        return tl.metric_correlation(self.data, **kwargs)

    def rank_agreement(self, **kwargs) -> pd.DataFrame:
        """Agreement of method rankings between metrics (see :func:`metricscape.tl.rank_agreement`)."""
        return tl.rank_agreement(self.data[self.data["control_group"] == "non-control method"], **kwargs)

    def control_separation(self) -> pd.Series:
        """Positive-vs-negative control separation per metric (see :func:`metricscape.tl.control_separation`)."""
        return tl.control_separation(self.data)

    def plot_response(self, metric: str, covariate: str, **kwargs):
        """Plot ``metric`` against ``covariate`` per method (see :func:`metricscape.pl.response_grid`)."""
        return pl.response_grid(self.data, metric, covariate, **kwargs)
