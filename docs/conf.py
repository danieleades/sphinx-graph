project = "sphinx-graph"
copyright = "2022, danieleades <danieleades@hotmail.com>"
author = "danieleades <danieleades@hotmail.com>"

extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx_rtd_theme",
    "sphinx_graph",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

myst_enable_extensions = [
    "colon_fence",
]