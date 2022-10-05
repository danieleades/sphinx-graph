from typing import Sequence
from sphinx_graph import Config, FormatHelper
from docutils import nodes


# -- Project information -----------------------------------------------------

project = "test"
copyright = "2022, daniel.eades"
author = "daniel.eades"


# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx_graph",
]

templates_path = ["_templates"]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
html_theme = "alabaster"

html_static_path = ["_static"]


def format_custom(helper: FormatHelper) -> Sequence[nodes.Node]:
    line_block = nodes.line_block()

    line_block += nodes.line("", f"UID: {helper.uid}")

    if helper.parents:
        line_block += helper.parent_list()

    if helper.children:
        line_block += helper.child_list()

    return [line_block, helper.content]


sphinx_config = Config(
    custom_layouts={
        "custom": format_custom
    },
)
