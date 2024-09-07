"""Types and methods specific to the vertex directive."""

from docutils import nodes
from sphinx.application import Sphinx

from . import events
from .config import Config
from .directive import Directive
from .info import Info
from .node import VertexNode
from .query import Query
from .state import State

__all__ = [
    "Config",
    "Info",
    "Query",
    "State",
    "VertexNode",
]


def visit_node(_self: nodes.GenericNodeVisitor, _node: nodes.Node) -> None:
    """Visits the Vertex node.

    This method is a no-op
    """


def depart_node(_self: nodes.GenericNodeVisitor, _node: nodes.Node) -> None:
    """Visits the Vertex node.

    This method is a no-op
    """


def register(app: Sphinx) -> None:
    """Register the vertex node, directive, and events."""
    app.add_node(
        VertexNode,
        html=(visit_node, depart_node),
        latex=(visit_node, depart_node),
        text=(visit_node, depart_node),
    )

    app.add_directive("vertex", Directive)

    events.register(app)
