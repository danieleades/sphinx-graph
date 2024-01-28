"""Lifecycle events specific to the vertex-table directive."""

from __future__ import annotations

from typing import TYPE_CHECKING

from docutils import nodes
from sphinx.errors import ConfigError

from sphinx_graph import vertex
from sphinx_graph.format import comma_separated_list
from sphinx_graph.table.node import TableNode
from sphinx_graph.table.state import State
from sphinx_graph.vertex.events import relative_uris, vertex_reference
from sphinx_graph.vertex.query import DEFAULT_QUERY, QUERIES

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sphinx.application import Sphinx
    from sphinx.builders import Builder

__all__ = [
    "register",
]


def relatives(
    builder: Builder,
    docname: str,
    state: vertex.State,
    uid: str,
) -> tuple[Iterable[nodes.reference], Iterable[nodes.reference]]:
    """Find the realtive URIs of the immediate 'relatives' of a given vertex.

    Args:
        builder: The sphinx builder instance
        docname: the name of the current document
        state: the global vertex information
        uid: the UID of the vertex

    Returns:
        a tuple of (parents, children) where each is an iterable over
        (target_uid, relative_uri)
    """
    info = state.vertices[uid]
    [parents, children] = [
        relative_uris(builder, docname, state.vertices, uids)
        for uids in [info.parents.keys(), state.children(uid)]
    ]
    return (parents, children)


def process(app: Sphinx, doctree: nodes.document, _fromdocname: str) -> None:
    """Process Vertex nodes by formatting and adding links to graph neighbours."""
    builder = app.builder
    state = State.read(app.env)
    vertex_state = vertex.State.read(app.env)
    queries = QUERIES
    queries.update(app.config.graph_config.queries)
    for node in doctree.findall(TableNode):
        uid = node["graph_uid"]
        info = state.tables[uid]
        if info.query and info.query not in queries:
            msg = f"no query registered with name '{info.query}'"
            raise ConfigError(msg)
        query = queries[info.query or DEFAULT_QUERY]
        vertices = query(vertex_state, **info.args)
        table = build_vertex_table(builder, info.docname, vertex_state, vertices)
        node.replace_self(table)


def build_table(
    headers: list[str],
    items: list[dict[str, nodes.paragraph]],
) -> nodes.table:
    """Construct a docutils nodes.table from a header and a list of dicts.

    Args:
        headers: a list of column headers, in order
        items: the rows of the table. The keys should match the headers. Missing keys
            are represented using an empty cell.
    """
    table = nodes.table()
    tgroup = nodes.tgroup()
    thead = nodes.thead()
    thead_row = nodes.row()
    thead += thead_row
    tbody = nodes.tbody()

    for header in headers:
        colspec = nodes.colspec(colwidth=1)
        tgroup += colspec
        entry = nodes.entry()
        entry += nodes.paragraph(text=header)
        thead_row += entry

    for item in items:
        row = nodes.row()
        tbody += row
        for header in headers:
            entry = nodes.entry()
            entry += item.get(header, nodes.paragraph())
            row += entry

    table += tgroup
    tgroup += thead
    tgroup += tbody

    return table


def build_vertex_table(
    builder: Builder,
    docname: str,
    state: vertex.State,
    vertices: Iterable[str],
) -> nodes.table:
    """Construct a table from a list of vertices."""
    headers = ["uid", "tags", "parents", "children"]
    items: list[dict[str, nodes.paragraph]] = []
    for uid in vertices:
        uid_para = nodes.paragraph()
        uid_para += vertex_reference(builder, docname, state.vertices, uid)

        item = {
            "uid": uid_para,
            "tags": nodes.paragraph(text=", ".join(state.vertices[uid].tags)),
        }

        [parent_refs, child_refs] = relatives(builder, docname, state, uid)

        parents = nodes.paragraph()
        parents.extend(comma_separated_list(parent_refs))
        item["parents"] = parents

        children = nodes.paragraph()
        children.extend(comma_separated_list(child_refs))
        item["children"] = children

        items.append(item)

    return build_table(headers, items)


def register(app: Sphinx) -> None:
    """Register the vertex-table lifecycle events."""
    app.connect("doctree-resolved", process)
