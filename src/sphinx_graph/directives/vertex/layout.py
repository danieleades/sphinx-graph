"""Utilities for formatting vertices into docutils.nodes for insertion into the document."""

from __future__ import annotations

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


def format_default(
    uid: str, content: nodes.Node, children: list[nodes.Node], parents: list[nodes.Node]
) -> Sequence[nodes.Node]:
    title = nodes.subtitle()
    title.append(nodes.strong(text=uid))

    attributes = nodes.paragraph()
    if children:
        line = nodes.line()
        line.extend(children)
        emphasis = nodes.emphasis()
        emphasis.append(line)
        attributes.append(emphasis)

    if parents:
        line = nodes.line()
        line.extend(parents)
        emphasis = nodes.emphasis()
        emphasis.append(line)
        attributes.append(emphasis)

    return [title, attributes, content]


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
    paragraph = nodes.paragraph()

    line = nodes.line()
    line += nodes.Text(uid)

    if parents:
        line += nodes.Text(" | ")
        line.extend(parents)
    if children:
        line += nodes.Text(" | ")
        line.extend(children)

    emphasis = nodes.emphasis()
    emphasis.append(line)

    paragraph.append(emphasis)
    paragraph.append(content)
    return [paragraph]


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
        state, builder, info.docname, "parents: ", parent_ids
    )

    children = create_references_nodes(
        state, builder, info.docname, "children: ", info.children
    )

    return formatter(info.uid, info.node, children, parents)
