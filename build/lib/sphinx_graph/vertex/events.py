"""Lifecycle events specific to the Vertex node."""

from __future__ import annotations

from typing import TYPE_CHECKING

from docutils import nodes

from sphinx_graph.vertex import layout
from sphinx_graph.vertex.info import Info, InfoParsed
from sphinx_graph.vertex.node import VertexNode
from sphinx_graph.vertex.state import build_and_check_graph
from sphinx_graph.vertex.state import merge as state_merge
from sphinx_graph.vertex.state import purge as state_purge

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping

    from sphinx.application import Sphinx
    from sphinx.builders import Builder


def vertex_reference(
    builder: Builder,
    from_docname: str,
    vertices: Mapping[str, Info],
    target_uid: str,
) -> nodes.reference:
    """Construct a reference to a vertex.

    Args:
        builder: The current sphinx 'builder'
        from_docname: The name of the document where the reference is located (the
            source)
        vertices: A mapping from vertex UID to vertex Info
        target_uid: The UID of the target vertex

    Returns:
        A nodes.reference, ready for insertion into the document
    """
    uri = builder.get_relative_uri(from_docname, vertices[target_uid].docname)
    refuri = f"{uri}#{target_uid}"
    reference = nodes.reference(refuri=refuri)
    reference.append(nodes.Text(target_uid))
    return reference


def relative_uris(
    builder: Builder,
    from_docname: str,
    vertices: Mapping[str, Info],
    target_uids: Iterable[str],
) -> Iterable[nodes.reference]:
    """Iterate over node UIDs and convert them to relative URIs."""
    return (
        vertex_reference(builder, from_docname, vertices, target_uid)
        for target_uid in target_uids
    )


def process(app: Sphinx, doctree: nodes.document, _fromdocname: str) -> None:
    """Process Vertex nodes by formatting and adding links to graph neighbours."""
    builder = app.builder
    state = build_and_check_graph(app.env)
    for vertex_node in doctree.findall(VertexNode):
        uid = vertex_node["graph_uid"]
        info = state.vertices[uid]
        [parents, children] = [
            relative_uris(builder, info.docname, state.vertices, uids)
            for uids in [info.parents.keys(), state.children(uid)]
        ]
        parsed_info = InfoParsed(
            content=vertex_node.deepcopy(),
            parents=parents,
            children=children,
            tags=info.tags,
        )
        vertex_node.replace_self(
            layout.apply_formatting(
                uid,
                parsed_info,
                info.config.layout,
            ),
        )


def register(app: Sphinx) -> None:
    """Register the vertex directive lifecycle events."""
    app.connect("env-purge-doc", state_purge)
    app.connect("env-merge-info", state_merge)
    app.connect("doctree-resolved", process)
