"""Tools quantifying how metrics behave over a search space."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def metric_response(
    df: pd.DataFrame, covariate: str, min_points: int = 4, by: str = "method_id"
) -> pd.DataFrame:
    """Fit a linear response of each metric to a covariate, per method.

    Answers: *does this metric systematically drift as the covariate (e.g. batch
    imbalance) changes, independent of the method's actual quality?*

    Parameters
    ----------
    df
        Long score table that also contains the ``covariate`` column.
    covariate
        Column describing position in the search space.
    min_points
        Groups with fewer points, or no variation in the covariate, are skipped.
    by
        Grouping column besides ``metric_id``.

    Returns
    -------
    Table with ``metric_id``, ``by``, ``n``, ``slope``, ``pvalue`` and ``r2``.
    """
    rows = []
    for (metric, group), d in df.groupby(["metric_id", by]):
        d = d.dropna(subset=[covariate, "metric_value"])
        if len(d) < min_points or d[covariate].nunique() < 2:
            continue
        res = stats.linregress(d[covariate], d["metric_value"])
        rows.append(
            {"metric_id": metric, by: group, "n": len(d), "slope": res.slope, "pvalue": res.pvalue, "r2": res.rvalue**2}
        )
    return pd.DataFrame(rows, columns=["metric_id", by, "n", "slope", "pvalue", "r2"])


def _wide(df: pd.DataFrame) -> pd.DataFrame:
    return df.pivot_table(index=["dataset_id", "method_id"], columns="metric_id", values="metric_value")


def metric_correlation(df: pd.DataFrame, method: str = "spearman") -> pd.DataFrame:
    """Correlate metrics across all (dataset, method) runs.

    Parameters
    ----------
    df
        Long score table.
    method
        ``"spearman"``, ``"pearson"`` or ``"kendall"``.

    Returns
    -------
    Metric x metric correlation matrix.
    """
    return _wide(df).corr(method=method)


def rank_agreement(df: pd.DataFrame, method: str = "spearman") -> pd.DataFrame:
    """Compare how metrics rank methods, averaged over datasets.

    Parameters
    ----------
    df
        Long score table.
    method
        Rank correlation type (``"spearman"`` or ``"kendall"``).

    Returns
    -------
    Metric x metric matrix of correlation between mean-over-dataset method scores.
    """
    mean = df.groupby(["method_id", "metric_id"])["metric_value"].mean().unstack()
    return mean.corr(method=method)


def control_separation(df: pd.DataFrame) -> pd.Series:
    """Score how well each metric separates positive from negative controls.

    Requires ``control_type`` (see :func:`metricscape.pp.annotate_controls`). A good metric
    scores positive controls higher than negative ones.

    Returns
    -------
    Per-metric probability that a random positive-control score exceeds a random
    negative-control score (AUC; 0.5 = no separation), sorted descending.
    """
    out = {}
    for metric, d in df.groupby("metric_id"):
        pos = d.loc[d["control_type"] == "positive", "metric_value"].to_numpy()
        neg = d.loc[d["control_type"] == "negative", "metric_value"].to_numpy()
        if len(pos) == 0 or len(neg) == 0:
            out[metric] = np.nan
            continue
        diff = pos[:, None] - neg[None, :]
        out[metric] = ((diff > 0).sum() + 0.5 * (diff == 0).sum()) / diff.size
    return pd.Series(out, name="auc").sort_values(ascending=False)
