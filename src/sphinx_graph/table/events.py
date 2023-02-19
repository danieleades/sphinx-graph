"""Lifecycle events specific to the Vertex node."""

from __future__ import annotations

from typing import Iterable

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.builders import Builder

from sphinx_graph import vertex
from sphinx_graph.format import create_reference, reference_list
from sphinx_graph.table.info import Info
from sphinx_graph.table.node import Node
from sphinx_graph.table.state import State
from sphinx_graph.vertex.events import relative_uri, relative_uris


def relatives(
    builder: Builder, docname: str, state: vertex.State, uid: str
) -> tuple[Iterable[tuple[str, str]], Iterable[tuple[str, str]]]:
    info = state.vertices[uid]
    [parents, children] = [
        relative_uris(builder, docname, state.vertices, uids)
        for uids in [info.parents.keys(), state.graph.predecessors(uid)]
    ]
    return (parents, children)


def relative_refs(
    builder: Builder, docname: str, state: vertex.State, uid: str
) -> tuple[Iterable[nodes.Node], Iterable[nodes.Node]]:
    [parents, children] = [
        reference_list(refs) for refs in relatives(builder, docname, state, uid)
    ]
    return (
        parents,
        children,
    )


def process(app: Sphinx, doctree: nodes.document, _fromdocname: str) -> None:
    """Process Vertex nodes by formatting and adding links to graph neighbours."""
    builder = app.builder
    state = State.read(app.env)
    vertex_state = vertex.State.read(app.env)
    for node in doctree.findall(Node):
        uid = node["graph_uid"]
        info = state.tables[uid]
        table = build_vertex_table(
            builder, info, vertex_state, vertex_state.vertices.keys()
        )
        node.replace_self(table)


def build_table(
    headers: list[str], items: list[dict[str, nodes.paragraph]]
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
    builder: Builder, table_info: Info, state: vertex.State, vertices: Iterable[str]
) -> nodes.table:
    headers = ["uid", "parents", "children"]
    items: list[dict[str, nodes.Node]] = []
    for uid in vertices:
        [uid_target, uid_uri] = relative_uri(
            builder, table_info.docname, state.vertices, uid
        )
        uid_para = nodes.paragraph()
        uid_para += create_reference(uid_target, uid_uri)
        item = {"uid": uid_para}
        [parent_refs, child_refs] = relative_refs(
            builder, table_info.docname, state, uid
        )
        parents = nodes.paragraph()
        parents.extend(parent_refs)
        item["parents"] = parents
        children = nodes.paragraph()
        children.extend(child_refs)
        item["children"] = children

        items.append(item)

    return build_table(headers, items)


def register(app: Sphinx) -> None:
    app.connect("doctree-resolved", process)
