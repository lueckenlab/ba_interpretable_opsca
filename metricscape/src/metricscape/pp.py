"""Annotating score tables with method and metric semantics."""

from __future__ import annotations

import pandas as pd

#: Default roles of control methods in the batch-integration benchmark.
DEFAULT_CONTROLS: dict[str, str] = {
    "embed_cell_types": "positive",
    "embed_cell_types_jittered": "positive",
    "shuffle_integration": "negative",
    "shuffle_integration_by_batch": "negative",
    "shuffle_integration_by_cell_type": "negative",
    "no_integration": "baseline",
    "no_integration_batch": "baseline",
}

#: Default metric groups of the batch-integration benchmark.
DEFAULT_METRIC_TYPES: dict[str, str] = {
    **dict.fromkeys(
        ["ari", "nmi", "clisi", "cell_cycle_conservation", "asw_label", "isolated_label_f1", "isolated_label_asw"],
        "bio",
    ),
    **dict.fromkeys(
        ["pcr", "graph_connectivity", "ilisi", "asw_batch", "kbet_pg", "kbet_pg_label", "ari_batch", "nmi_batch"],
        "batch",
    ),
}


def annotate_controls(df: pd.DataFrame, controls: dict[str, str] | None = None) -> pd.DataFrame:
    """Label each method as positive/negative/baseline control or ``non-control``.

    Adds ``control_type`` and a coarse ``control_group`` (``"control method"`` vs
    ``"non-control method"``) so real methods can be analysed separately from controls.

    Parameters
    ----------
    df
        Long score table.
    controls
        Mapping method id -> control role; defaults to :data:`DEFAULT_CONTROLS`.
    """
    controls = DEFAULT_CONTROLS if controls is None else controls
    out = df.copy()
    out["control_type"] = out["method_id"].map(controls).fillna("non-control")
    out["control_group"] = out["control_type"].map(lambda x: "non-control method" if x == "non-control" else "control method")
    return out


def annotate_metric_types(
    df: pd.DataFrame, metric_types: dict[str, str] | None = None, default: str = "other"
) -> pd.DataFrame:
    """Add a ``metric_type`` column (e.g. ``bio`` or ``batch``) to a score table.

    Parameters
    ----------
    df
        Long score table.
    metric_types
        Mapping metric id -> type; defaults to :data:`DEFAULT_METRIC_TYPES`.
    default
        Type for unmapped metrics.
    """
    metric_types = DEFAULT_METRIC_TYPES if metric_types is None else metric_types
    out = df.copy()
    out["metric_type"] = out["metric_id"].map(metric_types).fillna(default)
    return out
