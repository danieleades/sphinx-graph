"""Lifecycle events specific to the Vertex node."""

from __future__ import annotations

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.util import logging

from sphinx_graph.node import Node as VertexNode
from sphinx_graph.state import State
from sphinx_graph.util import unwrap

logger = logging.getLogger(__name__)

__all__ = [
    "process",
    "purge",
    "merge",
]


def process(app: Sphinx, doctree: nodes.document, _fromdocname: str) -> None:
    """Process Vertex nodes by formatting and adding links to graph neighbours."""
    builder = unwrap(app.builder)
    env = unwrap(builder.env)

    with State.get(env) as state:
        for vertex_node in doctree.findall(VertexNode):
            uid = vertex_node["graph_uid"]
            content = state.all_vertices[uid].content

            new_content = nodes.Element()
            new_content.append(nodes.Text(f"---start vertex {uid}---"))
            new_content.append(content)
            new_content.append(
                nodes.line(f"---end vertex {uid}---", f"---end vertex {uid}---")
            )
            vertex_node.replace_self(new_content)


def purge(_app: Sphinx, env: BuildEnvironment, docname: str) -> None:
    """
    Clear out all vertices whose docname matches the given one from the graph_all_vertices list.

    If there are vertices left in the document, they will be added again during parsing.
    """
    with State.get(env) as state:
        state.all_vertices = {
            id: vert
            for id, vert in state.all_vertices.items()
            if vert.docname != docname
        }


def merge(
    _app: Sphinx, env: BuildEnvironment, _docnames: list[str], other: BuildEnvironment
) -> None:
    """Merge the vertices from multiple environments during parallel builds."""
    with State.get(env) as state, State.get(other) as other_state:
        state.all_vertices.update(other_state.all_vertices)
