"""Sphinx Directive for Vertex objects."""

from __future__ import annotations

from typing import Sequence

from docutils import nodes
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import nested_parse_with_titles

from sphinx_graph.info import Info
from sphinx_graph.node import Node as VertexNode
from sphinx_graph.state import State

__all__ = [
    "Directive",
]


class Directive(SphinxDirective):
    """An RST node representing a To-Do item."""

    has_content = True
    required_arguments = 1

    def run(self) -> Sequence[nodes.Node]:
        """Run the directive and return a Vertex node."""

        content_node = nodes.Element()
        nested_parse_with_titles(self.state, self.content, content_node)

        uid = self.arguments[0]

        placeholder_node = VertexNode(graph_uid=uid)

        with State.get(self.env) as state:
            state.insert_vertex(
                uid,
                Info(
                    docname=self.env.docname,
                    content=content_node,
                ),
            )

        return [placeholder_node]
