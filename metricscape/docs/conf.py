"""Sphinx configuration."""

project = "metricscape"
extensions = ["myst_nb", "sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx.ext.autosummary", "sphinx_autodoc_typehints", "sphinx_copybutton"]
autosummary_generate = True
html_theme = "sphinx_book_theme"
exclude_patterns = ["_build"]
