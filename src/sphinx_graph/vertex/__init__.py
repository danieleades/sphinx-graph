"""Types and methods specific to the vertex directive."""

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


def register(app: Sphinx) -> None:
    """Register the vertex node, directive, and events."""
    app.add_node(
        Node,
    )

    app.add_directive("vertex", Directive)

    events.register(app)
