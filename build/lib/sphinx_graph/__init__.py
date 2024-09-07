"""Sphinx-Graph public API.

add the sphinx-graph extension to your sphinx project by
adding it to ``conf.py``:

.. code:: python

    extensions = [
        "sphinx_graph",
    ]
"""

from typing import TypedDict

from sphinx.application import Sphinx

from . import table, vertex
from .config import Config
from .vertex import Config as VertexConfig
from .vertex import Query

__all__ = [
    "Config",
    "Query",
    "VertexConfig",
    "vertex",
]


class ExtensionMetadata(TypedDict):
    """The metadata returned by this extension."""

    version: str
    env_version: int
    parallel_read_safe: bool
    parallel_write_safe: bool


def setup(app: Sphinx) -> ExtensionMetadata:
    """Set up the sphinx-graph extension."""
    app.add_config_value("graph_config", Config(), "", types=Config)

    vertex.register(app)
    table.register(app)

    return {
        "version": "0.1",
        "env_version": 0,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
