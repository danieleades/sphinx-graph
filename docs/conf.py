import re

from sphinx_graph import Config, VertexConfig

project = "sphinx-graph"
copyright = "2022, danieleades <danieleades@hotmail.com>"
author = "danieleades <danieleades@hotmail.com>"

extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx_rtd_theme",
    "sphinx_graph",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"

graph_config = Config(
    types={
        "mrd": VertexConfig(layout="transparent", regex=re.compile(r"^MRD-[0-9]{3}$")),
        "usr": VertexConfig(regex=re.compile(r"^USR-[0-9]{3}$")),
        "sys": VertexConfig(regex=re.compile(r"^SYS-[0-9]{3}$")),
    },
)
