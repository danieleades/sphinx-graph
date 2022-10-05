import os
import sys

from sphinx_graph import Config

sys.path.insert(0, os.path.abspath("."))
from custom_layout import format_custom  # noqa:E402

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


graph_config = Config(
    custom_layouts={"custom": format_custom},
)
