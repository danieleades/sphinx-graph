import re
import sys
from pathlib import Path

from sphinx_graph import Config, VertexConfig

sys.path.append(str(Path.cwd()))

import query

project = "sphinx-graph"
copyright = "2022, danieleades <danieleades@hotmail.com>"
author = "danieleades <danieleades@hotmail.com>"

extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx_rtd_theme",
    "sphinx_graph",
    "sphinx.ext.viewcode",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"

graph_config = Config(
    types={
        "mrd": VertexConfig(layout="transparent", regex=re.compile(r"^MRD-[0-9]{3}$")),
        "usr": VertexConfig(
            regex=re.compile(r"^USR-[0-9]{3}$"),
            # we require our user requirements to have parents because we want to show
            # traceability to the MRD
            require_parent=True,
        ),
        "sys": VertexConfig(
            regex=re.compile(r"^SYS-[0-9]{3}$"),
            # we require our system requirements to have parents because we want to show
            # traceability to the user requirements
            require_parent=True,
        ),
    },
    queries={
        "ancestors": query.ancestors,
        "descendants": query.descendants,
    },
)

autosummary_generate = True
autosummary_ignore_module_all = False
autoclass_content = "both"
autodoc_inherit_docstrings = True
set_type_checking_flag = True
add_module_names = True
templates_path = ["_templates"]
nitpick_ignore = {
    (
        # see https://github.com/sphinx-doc/sphinx/issues/12286
        "py:class",
        "rustworkx.PyDiGraph",
    ),
}
