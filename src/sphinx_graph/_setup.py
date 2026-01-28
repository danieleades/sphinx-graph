"""Sphinx extension setup."""

from typing import TypedDict

from sphinx.application import Sphinx

from . import table, vertex
from .config import Config


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
