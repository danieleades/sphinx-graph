"""Utilities for formatting vertices into docutils.nodes for insertion into the document."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Iterator, Sequence

from docutils import nodes
from sphinx.builders import Builder

from sphinx_graph.util import comma_separated_list
from sphinx_graph.vertex.info import InfoParsed
from sphinx_graph.vertex.state import State

__all__ = [
    "FORMATTERS",
    "DEFAULT_LAYOUT",
    "apply_formatting",
]


def format_reference(uid: str, reference: nodes.reference) -> nodes.reference:
    reference.append(nodes.Text(uid))
    return reference


def create_references(
    state: State, builder: Builder, from_docname: str, uids: Iterable[str]
) -> Iterator[nodes.Node]:
    for uid in uids:
        yield format_reference(uid, state.create_reference(builder, uid, from_docname))


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

    def _list(
        self, references: list[nodes.reference], prefix: str | None
    ) -> nodes.line | None:
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


def format_default(helper: FormatHelper) -> Sequence[nodes.Node]:
    line_block = nodes.line_block()

    line_block += nodes.line("", f"UID: {helper.uid}")

    line_block += helper.parent_list()
    line_block += helper.child_list()

    return [line_block, helper.content]


def format_transparent(helper: FormatHelper) -> Sequence[nodes.Node]:
    return [helper.content]


def format_subtle(helper: FormatHelper) -> Sequence[nodes.Node]:
    one_liner = nodes.subscript()

    one_liner += nodes.Text(helper.uid)

    if helper.parents:
        one_liner += nodes.Text(" | ")
        one_liner.extend(helper.parent_list())

    if helper.children:
        one_liner += nodes.Text(" | ")
        one_liner.extend(helper.child_list())

    paragraph = nodes.paragraph()
    paragraph += one_liner

    return [paragraph, helper.content]


Formatter = Callable[[FormatHelper], Sequence[nodes.Node]]
"""A function which formats a Vertex, ready for insertion into the document.

a Formatter is a Callable which accepts a FormatHelper and returns a Sequence of docutils Nodes.
"""

FORMATTERS: dict[str, Formatter] = {
    "default": format_default,
    "transparent": format_transparent,
    "subtle": format_subtle,
}

DEFAULT_LAYOUT = "default"


def apply_formatting(
    formatter: Formatter, state: State, builder: Builder, info: InfoParsed
) -> Sequence[nodes.Node]:
    """Apply the given formatter to create a vertex node ready for insertion."""
    parent_ids = (link.uid for link in info.parents)
    parents = list(create_references(state, builder, info.docname, parent_ids))

    children = list(create_references(state, builder, info.docname, info.children))

    helper = FormatHelper(info.uid, info.node, parents, children)

    return formatter(helper)
