from docutils import nodes
from sphinx.application import Sphinx

from sphinx_graph.vertex import events
from sphinx_graph.vertex.config import Config
from sphinx_graph.vertex.directive import Directive
from sphinx_graph.vertex.info import Info
from sphinx_graph.vertex.node import Node
from sphinx_graph.vertex.query import Query
from sphinx_graph.vertex.state import State

__all__ = [
    "Config",
    "Info",
    "Node",
    "State",
    "Query",
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

    app.add_directive("vertex", Directive)

    events.register(app)
