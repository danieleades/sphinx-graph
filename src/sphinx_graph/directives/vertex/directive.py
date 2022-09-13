"""Sphinx Directive for Vertex objects."""
from __future__ import annotations

import base64
import hashlib
from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence

from docutils import nodes
from sphinx.builders import Builder
from sphinx.util.docutils import SphinxDirective

from sphinx_graph import parse
from sphinx_graph.directives.vertex.info import Info, InfoParsed, Link
from sphinx_graph.directives.vertex.node import Node
from sphinx_graph.directives.vertex.state import State, get_state
from sphinx_graph.util import comma_separated_list

__all__ = [
    "Directive",
]


def parse_parents(input: str | None) -> list[Link]:
    """Parse a comma separated list of parent link specifications.

    each element in the list may be in one of two forms

    - {PARENT_ID}
    - {PARENT_ID}:{PARENT_FINGERPRINT}
    """
    tokens = parse.comma_separated_list(input)
    output: list[Link] = []
    for token in tokens:
        if ":" in token:
            subtokens = token.split(":", maxsplit=1)
            uid = subtokens[0]
            fingerprint = subtokens[1]
            output.append(Link(uid, fingerprint=fingerprint))
        else:
            output.append(Link(token, fingerprint=None))
    return output


@dataclass
class Args:
    """Parsed arguments for the Vertex directive."""

    uid: str
    parents: list[Link] = field(default_factory=list)


class Directive(SphinxDirective):
    """An RST node representing a To-Do item."""

    has_content = True
    required_arguments = 1
    option_spec = {
        "parents": parse_parents,
    }

    def run(self) -> Sequence[nodes.Node]:
        """Run the directive and return a Vertex node."""
        args = Args(uid=self.arguments[0], **self.options)

        text = "\n".join(self.content)

        fingerprint = base64.b64encode(hashlib.md5(text.encode()).digest())[:5].decode()

        content_node = Node(text)
        self.state.nested_parse(self.content, self.content_offset, content_node)

        targetnode = nodes.target("", "", ids=[args.uid])
        placeholder_node = Node(ids=[args.uid])

        with get_state(self.env) as state:
            state.insert_vertex(
                args.uid,
                Info(
                    docname=self.env.docname,
                    lineno=self.lineno,
                    node=content_node,
                    target=targetnode,
                    parents=args.parents,
                    fingerprint=fingerprint,
                ),
            )

        return [targetnode, placeholder_node]


def format_reference(uid: str, reference: nodes.reference) -> nodes.reference:
    reference.append(nodes.Text(uid))
    return reference


def create_references(
    state: State, builder: Builder, from_docname: str, uids: Iterable[str]
) -> Iterator[nodes.Node]:
    for uid in uids:
        reference = format_reference(
            uid, state.create_reference(builder, uid, from_docname)
        )
        yield reference


def create_references_para(
    state: State, builder: Builder, from_docname: str, prefix: str, uids: Iterable[str]
) -> nodes.paragraph:
    references = list(create_references(state, builder, from_docname, uids))
    if references:
        para = nodes.paragraph()
        para += nodes.Text(prefix)
        para.extend(comma_separated_list(references))
        return para
    return None


def format_node(state: State, builder: Builder, info: InfoParsed) -> nodes.Node:
    """Generate a formatted vertex, ready for insertion into the document."""
    table: nodes.Node = nodes.table()
    tgroup = nodes.tgroup(cols=1)
    colspec = nodes.colspec(colwidth=1)
    tgroup.append(colspec)
    table += tgroup

    # add header
    thead = nodes.thead()
    tgroup += thead
    row = nodes.row()
    entry = nodes.entry()
    entry += nodes.paragraph(text=f"Requirement: {info.uid}")
    row += entry
    thead.append(row)

    tbody = nodes.tbody()

    # add attributes
    row = nodes.row()
    entry = nodes.entry()

    parent_ids = (link.uid for link in info.parents)
    entry += create_references_para(
        state, builder, info.docname, "parents: ", parent_ids
    )

    entry += create_references_para(
        state, builder, info.docname, "children: ", info.children
    )

    row += entry
    tbody.append(row)

    # add content
    row = nodes.row()
    entry = nodes.entry()
    entry += info.node
    row += entry

    tbody.append(row)

    tgroup += tbody

    return table
