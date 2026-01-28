"""Registration of the vertex node, directive, and events."""

from docutils import nodes
from sphinx.application import Sphinx

from . import events
from .directive import Directive
from .node import VertexNode


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
