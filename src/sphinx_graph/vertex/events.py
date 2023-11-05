"""Lifecycle events specific to the Vertex node."""

from __future__ import annotations

from collections.abc import Iterable

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.environment import BuildEnvironment

from sphinx_graph.vertex import layout
from sphinx_graph.vertex.info import Info, InfoParsed
from sphinx_graph.vertex.node import VertexNode
from sphinx_graph.vertex.state import State


def vertex_reference(
    builder: Builder,
    from_docname: str,
    vertices: dict[str, Info],
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
    vertices: dict[str, Info],
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
    with State.get(app.env) as state:
        state.build_and_check_graph()
        for vertex_node in doctree.findall(VertexNode):
            uid = vertex_node["graph_uid"]
            info = state.vertices[uid]
            [parents, children] = [
                relative_uris(builder, info.docname, state.vertices, uids)
                for uids in [info.parents.keys(), state.graph.successors(uid)]
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


def purge(_app: Sphinx, env: BuildEnvironment, docname: str) -> None:
    """Clear out all stale vertices.

    All vertices whose docname matches the given one from the graph_all_vertices list
    will be removed.

    If there are vertices left in the document, they will be added again during parsing.
    """
    with State.get(env) as state:
        state.vertices = {
            uid: vert for uid, vert in state.vertices.items() if vert.docname != docname
        }


def merge(
    _app: Sphinx,
    env: BuildEnvironment,
    _docnames: list[str],
    other: BuildEnvironment,
) -> None:
    """Merge the vertices from multiple environments during parallel builds."""
    with State.get(env) as state, State.get(other) as other_state:
        state.vertices.update(other_state.vertices)


def register(app: Sphinx) -> None:
    """Register the vertex directive lifecycle events."""
    app.connect("doctree-resolved", process)
    app.connect("env-purge-doc", purge)
    app.connect("env-merge-info", merge)
