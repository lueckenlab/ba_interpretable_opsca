"""Plotting helpers."""

from __future__ import annotations

import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


def response_grid(df: pd.DataFrame, metric: str, covariate: str, methods: list[str] | None = None, ncols: int = 3):
    """Scatter a metric against a covariate with one panel per method.

    Each panel shows a regression line and its R² / p-value.

    Parameters
    ----------
    df
        Long score table containing the covariate.
    metric
        Metric id to show.
    covariate
        Column on the x axis.
    methods
        Methods to show (default: all present).
    ncols
        Panels per row.

    Returns
    -------
    The matplotlib figure.
    """
    d = df[df["metric_id"] == metric]
    methods = sorted(d["method_id"].unique()) if methods is None else methods
    nrows = max(1, math.ceil(len(methods) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4 * nrows), squeeze=False)
    axes = axes.ravel()
    for ax, method in zip(axes, methods, strict=False):
        dm = d[d["method_id"] == method].dropna(subset=[covariate, "metric_value"])
        ax.scatter(dm[covariate], dm["metric_value"], alpha=0.7)
        title = method
        if len(dm) >= 3 and dm[covariate].nunique() > 1:
            res = stats.linregress(dm[covariate], dm["metric_value"])
            xs = np.linspace(dm[covariate].min(), dm[covariate].max(), 100)
            ax.plot(xs, res.intercept + res.slope * xs, linewidth=2)
            title += f"\n$R^2$={res.rvalue**2:.2f}, p={res.pvalue:.2g}"
        ax.set(xlabel=covariate, ylabel=metric, title=title)
    for ax in axes[len(methods):]:
        ax.set_visible(False)
    fig.tight_layout()
    return fig


def heatmap(matrix: pd.DataFrame, title: str = "", cmap: str = "coolwarm", vmin=-1, vmax=1):
    """Plot a square matrix (e.g. from :func:`metricscape.tl.metric_correlation`).

    Returns
    -------
    The matplotlib axes.
    """
    fig, ax = plt.subplots(figsize=(0.6 * len(matrix) + 2, 0.6 * len(matrix) + 1))
    im = ax.imshow(matrix.to_numpy(), cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_xticks(range(len(matrix.columns)), matrix.columns, rotation=90)
    ax.set_yticks(range(len(matrix.index)), matrix.index)
    ax.set_title(title)
    fig.colorbar(im, ax=ax)
    return ax
