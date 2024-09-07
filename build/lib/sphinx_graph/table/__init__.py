"""Types and methods specific to the vertex-table directive."""

from docutils import nodes
from sphinx.application import Sphinx

from . import events
from .directive import Directive
from .info import Info
from .node import TableNode

__all__ = [
    "Directive",
    "Info",
    "TableNode",
    "register",
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
    """Register the vertex-table node, directive, and lifecycle events."""
    app.add_node(
        TableNode,
        html=(visit_node, depart_node),
        latex=(visit_node, depart_node),
        text=(visit_node, depart_node),
    )

    app.add_directive("vertex-table", Directive)

    events.register(app)
