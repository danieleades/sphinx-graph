"""Utilities for formatting vertices into docutils.nodes for insertion into the document."""

from __future__ import annotations
from dataclasses import dataclass

from typing import Callable, Iterable, Iterator, List, Sequence

from docutils import nodes
from sphinx.builders import Builder

from sphinx_graph.directives.vertex.info import InfoParsed
from sphinx_graph.directives.vertex.state import State
from sphinx_graph.util import comma_separated_list

__all__ = [
    "FORMATTERS",
    "DEFAULT_FORMATTER",
    "apply_formatting",
]


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


def create_references_nodes(
    state: State, builder: Builder, from_docname: str, prefix: str, uids: Iterable[str]
) -> list[nodes.Node]:
    text: list[nodes.Node] = []
    references = list(create_references(state, builder, from_docname, uids))
    if references:
        text.append(nodes.Text(prefix))
        text.extend(comma_separated_list(references))
        return text
    return []


@dataclass
class FormatHelper:
    """Helper class for formatting a Vertex.

    Args:
        uid: the unique identifier of the vertex
        content: the nested content of the vertex
        parents: a list of references to parent Vertices
        children: a list of references to child Vertices
    """

    uid: str
    content: nodes.Node
    parents: list[nodes.reference]
    children: list[nodes.reference]

    def _list(self, references: list[nodes.reference], prefix: str | None) -> nodes.line | None:
        if not references:
            return None

        line = nodes.line()
        if prefix:
            line += nodes.Text(prefix)
        line.extend(comma_separated_list(references))

        return line

    def child_list(self, prefix: str | None = "Children: ") -> nodes.line | None:
        """Format the list of child vertex references as a comma-separated list.

        Args:
            prefix: Optionally set a prefix for the list
        """
        return self._list(self.children, prefix)

    def parent_list(self, prefix: str | None = "Parents: ") -> nodes.line | None:
        """Format the list of parent vertex references as a comma-separated list.

        Args:
            prefix: Optionally set a prefix for the list
        """
        return self._list(self.parents, prefix)


def format_default(
    uid: str, content: nodes.Node, children: list[nodes.Node], parents: list[nodes.Node]
) -> Sequence[nodes.Node]:
    line_block = nodes.line_block()

    line_block += nodes.line("", f"UID: {uid}")

    if parents:
        line_block += nodes.line("", "", *parents)

    if children:
        line_block += nodes.line("", "", *children)

    return [line_block, content]


def format_transparent(
    _uid: str,
    content: nodes.Node,
    _children: list[nodes.Node],
    _parents: list[nodes.Node],
) -> Sequence[nodes.Node]:
    return [content]


def format_subtle(
    uid: str, content: nodes.Node, children: list[nodes.Node], parents: list[nodes.Node]
) -> Sequence[nodes.Node]:
    one_liner = nodes.subscript()

    one_liner += nodes.Text(uid)

    if parents:
        one_liner += nodes.Text(" | ")
        one_liner.extend(parents)

    if children:
        one_liner += nodes.Text(" | ")
        one_liner.extend(children)

    paragraph = nodes.paragraph()
    paragraph += one_liner

    return [paragraph, content]


Formatter = Callable[
    [str, nodes.Node, List[nodes.Node], List[nodes.Node]], Sequence[nodes.Node]
]

FORMATTERS: dict[str, Formatter] = {
    "default": format_default,
    "transparent": format_transparent,
    "subtle": format_subtle,
}

DEFAULT_FORMATTER = "default"


def apply_formatting(
    formatter: Formatter, state: State, builder: Builder, info: InfoParsed
) -> Sequence[nodes.Node]:
    """Apply the given formatter to create a vertex node ready for insertion."""
    parent_ids = (link.uid for link in info.parents)
    parents = create_references_nodes(
        state, builder, info.docname, "Parents: ", parent_ids
    )

    children = create_references_nodes(
        state, builder, info.docname, "Children: ", info.children
    )

    return formatter(info.uid, info.node, children, parents)
