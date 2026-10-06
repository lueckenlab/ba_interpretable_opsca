"""Reading benchmark scores into the canonical long-format table."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import pandas as pd
import yaml

#: Columns every score table must contain.
SCORE_COLUMNS = ("dataset_id", "method_id", "metric_id", "metric_value")


def read_scores_yaml(
    path: str | Path,
    keep_methods: Iterable[str] | None = None,
    drop_metrics: Iterable[str] = (),
) -> pd.DataFrame:
    """Read an OpenProblems-style ``score_uns.yaml`` into a long score table.

    Each yaml entry holds one (dataset, method) run with parallel lists
    ``metric_ids`` and ``metric_values``; these are expanded to one row per metric.

    Parameters
    ----------
    path
        Path to the yaml file.
    keep_methods
        If given, only these methods (case-insensitive) are kept.
    drop_metrics
        Metric ids to drop.

    Returns
    -------
    Table with columns :data:`SCORE_COLUMNS`; missing values and the last path
    component of ``dataset_id`` are cleaned.
    """
    with open(path) as f:
        data = yaml.safe_load(f)
    keep = None if keep_methods is None else {m.lower() for m in keep_methods}
    rows = []
    for entry in data:
        method = str(entry.get("method_id", "")).strip().lower()
        if keep is not None and method not in keep:
            continue
        for m_id, m_val in zip(entry.get("metric_ids", []), entry.get("metric_values", []), strict=False):
            rows.append(
                {
                    "dataset_id": entry.get("dataset_id"),
                    "method_id": method,
                    "metric_id": m_id,
                    "metric_value": m_val,
                }
            )
    return read_scores(pd.DataFrame(rows, columns=list(SCORE_COLUMNS)), drop_metrics=drop_metrics)


def read_scores(df: pd.DataFrame, drop_metrics: Iterable[str] = ()) -> pd.DataFrame:
    """Validate and clean a long-format score table.

    Parameters
    ----------
    df
        Table with at least the columns :data:`SCORE_COLUMNS`.
    drop_metrics
        Metric ids to remove.

    Returns
    -------
    A cleaned copy: NaN scores and ``drop_metrics`` removed, dataset ids reduced to their basename.
    """
    missing = set(SCORE_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    out = df.dropna(subset=["metric_value"]).copy()
    out = out[~out["metric_id"].isin(list(drop_metrics))]
    out["dataset_id"] = out["dataset_id"].astype(str).str.split("/").str[-1]
    return out.reset_index(drop=True)
