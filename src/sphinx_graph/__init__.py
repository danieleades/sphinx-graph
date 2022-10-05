"""Sphinx-Graph public API.

add the sphinx-graph extension to your sphinx project by
adding it to ``conf.py``:

.. code:: python

    extensions = [
        "sphinx_graph",
    ]
"""

from typing import TypedDict

from docutils import nodes
from sphinx.application import Sphinx

from sphinx_graph.config import Config
from sphinx_graph.directives import vertex
from sphinx_graph.directives.vertex.layout import FormatHelper, Formatter
from sphinx_graph.util import unwrap

__all__ = [
    "Config",
    "Formatter",
    "FormatHelper",
]


def generate_graph(app: Sphinx, _doctree: nodes.document, _fromdocname: str) -> None:
    """Generate a graph of all vertices in the document."""
    builder = unwrap(app.builder)
    env = unwrap(builder.env)

    with vertex.get_state(env) as state:
        state.build_graph()


def check_graph_consistency(app: Sphinx, _exception: Exception) -> None:
    builder = unwrap(app.builder)
    env = unwrap(builder.env)

    config: Config = app.config.graph_config

    with vertex.get_state(env) as state:
        state.consistency_checks(config.require_fingerprints)


class ExtensionMetadata(TypedDict):
    """The metadata returned by this extension."""

    version: str
    env_version: int
    parallel_read_safe: bool
    parallel_write_safe: bool


def setup(app: Sphinx) -> ExtensionMetadata:
    """Set up the sphinx-graph extension."""
    app.add_config_value("graph_config", Config(), "", types=(Config))

    app.add_node(
        vertex.Node,
        html=(vertex.visit_node, vertex.depart_node),
        latex=(vertex.visit_node, vertex.depart_node),
        text=(vertex.visit_node, vertex.depart_node),
    )

    app.add_directive("vertex", vertex.Directive)
    app.connect("doctree-resolved", generate_graph)
    app.connect("doctree-resolved", vertex.process)
    app.connect("env-purge-doc", vertex.purge)
    app.connect("env-merge-info", vertex.merge)
    app.connect("build-finished", check_graph_consistency)

    return {
        "version": "0.1",
        "env_version": 0,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
