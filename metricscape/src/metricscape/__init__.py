"""Exploratory evaluation of benchmark metrics over real or simulated search spaces."""

from importlib.metadata import PackageNotFoundError, version

from . import io, pl, pp, sim, tl
from .explorer import MetricExplorer

try:
    __version__ = version("metricscape")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

__all__ = ["io", "pl", "pp", "sim", "tl", "MetricExplorer", "__version__"]
