"""Sphinx extension setup."""

from pathlib import Path
from typing import TypedDict

from sphinx.application import Sphinx
from sphinx.config import Config as SphinxConfig

from . import table, vertex
from .config import Config

_STATIC_DIR = Path(__file__).parent / "static"
_CSS_FILENAME = "sphinx-graph.css"

_LATEX_PREAMBLE = (
    r"\expandafter\providecommand\csname DUrolesphinx-graph-subtle\endcsname"
    r"[1]{{\small #1}}"
    "\n"
)


class ExtensionMetadata(TypedDict):
    """The metadata returned by this extension."""

    version: str
    env_version: int
    parallel_read_safe: bool
    parallel_write_safe: bool


def _add_latex_preamble(_app: Sphinx, config: SphinxConfig) -> None:
    existing = config.latex_elements.get("preamble", "")
    config.latex_elements["preamble"] = existing + _LATEX_PREAMBLE


def _register_static_path(app: Sphinx) -> None:
    app.config.html_static_path.append(str(_STATIC_DIR))


def setup(app: Sphinx) -> ExtensionMetadata:
    """Set up the sphinx-graph extension."""
    app.add_config_value("graph_config", Config(), "", types=Config)

    app.add_css_file(_CSS_FILENAME)
    app.connect("builder-inited", _register_static_path)
    app.connect("config-inited", _add_latex_preamble)

    vertex.register(app)
    table.register(app)

    return {
        "version": "0.1",
        "env_version": 0,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
