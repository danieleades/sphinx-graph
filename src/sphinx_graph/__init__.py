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

from sphinx_graph import events
from sphinx_graph.directive import Directive
from sphinx_graph.node import Node

__all__ = [
    "Config",
    "Formatter",
    "FormatHelper",
]


class ExtensionMetadata(TypedDict):
    """The metadata returned by this extension."""

    version: str
    env_version: int
    parallel_read_safe: bool
    parallel_write_safe: bool


def visit_node(_self: nodes.GenericNodeVisitor, _node: Node) -> None:
    """
    Visits the Vertex node.

    This method is a no-op
    """


def depart_node(_self: nodes.GenericNodeVisitor, _node: Node) -> None:
    """
    Visits the Vertex node.

    This method is a no-op
    """


def setup(app: Sphinx) -> ExtensionMetadata:
    """Set up the sphinx-graph extension."""

    app.add_node(
        Node,
        html=(visit_node, depart_node),
        latex=(visit_node, depart_node),
        text=(visit_node, depart_node),
    )

    app.add_directive("vertex", Directive)
    app.connect("doctree-resolved", events.process)
    app.connect("env-purge-doc", events.purge)
    app.connect("env-merge-info", events.merge)

    return {
        "version": "0.1",
        "env_version": 0,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
