"""Types and methods specific to the vertex-table directive"""

from docutils import nodes
from sphinx.application import Sphinx

from sphinx_graph.table import events
from sphinx_graph.table.directive import Directive
from sphinx_graph.table.info import Info
from sphinx_graph.table.node import Node

__all__ = [
    "Info",
    "Directive",
    "Node",
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
    app.add_node(
        Node,
        html=(visit_node, depart_node),
        latex=(visit_node, depart_node),
        text=(visit_node, depart_node),
    )

    app.add_directive("vertex-table", Directive)

    events.register(app)
