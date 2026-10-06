"""Real and simulated search spaces over which metrics are explored.

A *search space* is a table with one row per point (e.g. a dataset) and one column per
covariate (e.g. batch imbalance). A real space comes from dataset metadata; a simulated
space is sampled from parameter ranges, and metric behaviour is generated from a user
supplied response function.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class SearchSpace:
    """Named covariate ranges defining a simulated search space.

    Parameters
    ----------
    ranges
        Mapping covariate name -> ``(low, high)`` bounds.
    """

    ranges: Mapping[str, tuple[float, float]]

    def grid(self, n: int = 10) -> pd.DataFrame:
        """Return a regular grid with ``n`` values per covariate (``n ** d`` points)."""
        axes = [np.linspace(lo, hi, n) for lo, hi in self.ranges.values()]
        mesh = np.meshgrid(*axes, indexing="ij")
        return pd.DataFrame({k: m.ravel() for k, m in zip(self.ranges, mesh, strict=True)})

    def sample(self, n: int = 100, seed: int | None = 0) -> pd.DataFrame:
        """Draw ``n`` uniformly random points from the space."""
        rng = np.random.default_rng(seed)
        return pd.DataFrame({k: rng.uniform(lo, hi, n) for k, (lo, hi) in self.ranges.items()}).rename_axis(None)


def simulate_scores(
    space: pd.DataFrame,
    responses: Mapping[tuple[str, str], Callable[[pd.DataFrame], np.ndarray]],
    noise: float = 0.0,
    seed: int | None = 0,
) -> pd.DataFrame:
    """Simulate a long score table over a search space.

    Parameters
    ----------
    space
        Points of the search space, one per row (see :meth:`SearchSpace.grid`/``sample``).
        Each row becomes a pseudo dataset ``"sim_<i>"`` carrying its covariates.
    responses
        Mapping ``(method_id, metric_id)`` -> function taking the space and returning the
        expected metric value for each point.
    noise
        Standard deviation of Gaussian noise added to every score.
    seed
        Random seed.

    Returns
    -------
    Long score table (see :data:`metricscape.io.SCORE_COLUMNS`) merged with the covariates.
    """
    rng = np.random.default_rng(seed)
    base = space.reset_index(drop=True).copy()
    base.insert(0, "dataset_id", [f"sim_{i}" for i in range(len(base))])
    frames = []
    for (method, metric), fn in responses.items():
        values = np.asarray(fn(space), dtype=float) + rng.normal(0, noise, len(base))
        frames.append(base.assign(method_id=method, metric_id=metric, metric_value=values))
    return pd.concat(frames, ignore_index=True)
