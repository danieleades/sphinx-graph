"""Lifecycle events specific to the Vertex node."""

from __future__ import annotations

from typing import Iterable

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.environment import BuildEnvironment

from sphinx_graph import layout
from sphinx_graph.info import Info
from sphinx_graph.node import Node as VertexNode
from sphinx_graph.state import State, build_and_check_graph

__all__ = [
    "process",
    "purge",
    "merge",
]


def relative_uris(
    builder: Builder,
    from_docname: str,
    vertices: dict[str, Info],
    target_uids: Iterable[str],
) -> Iterable[tuple[str, str]]:
    """Iterate over node UIDs and convert them to relative URIs."""
    for target_uid in target_uids:
        relative_uri = builder.get_relative_uri(
            from_docname, vertices[target_uid].docname
        )
        yield (target_uid, relative_uri)


def process(app: Sphinx, doctree: nodes.document, _fromdocname: str) -> None:
    """Process Vertex nodes by formatting and adding links to graph neighbours."""
    builder = app.builder
    with State.get(app.env) as state:
        graph = build_and_check_graph(state.all_vertices)
        for vertex_node in doctree.findall(VertexNode):
            uid = vertex_node["graph_uid"]
            info = state.all_vertices[uid]
            [parents, children] = [
                relative_uris(builder, info.docname, state.all_vertices, uids)
                for uids in [info.parents.keys(), graph.predecessors(uid)]
            ]
            vertex_node.replace_self(
                layout.apply_formatting(
                    uid, vertex_node.deepcopy(), parents, children, info.config.layout
                )
            )


def purge(_app: Sphinx, env: BuildEnvironment, docname: str) -> None:
    """Clear out all vertices whose docname matches the given one from the graph_all_vertices list.

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
