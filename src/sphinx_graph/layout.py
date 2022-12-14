"""Tools and methods for formatting vertex nodes into docutils nodes."""

from __future__ import annotations

from typing import Callable, Iterable, TypeVar

from docutils import nodes
from sphinx.util import logging

logger = logging.getLogger(__name__)

__all__ = [
    "FormatHelper",
    "Formatter",
    "LAYOUTS",
    "DEFAULT",
]

DEFAULT = "subtle"


T = TypeVar("T")


def intersperse(iterable: Iterable[T], delimiter: T) -> Iterable[T]:
    """Intersperse objects in an iterator with another value of the same type."""
    for i, item in enumerate(iterable):
        if i != 0:
            yield delimiter
        yield item


def comma_separated_list(items: Iterable[nodes.Node]) -> Iterable[nodes.Node]:
    """Convert a sequence of docutils nodes into a comma separated list."""
    yield from intersperse(items, nodes.Text(", "))


def create_reference(target_uid: str, relative_uri: str) -> nodes.reference:
    """Create a docutils 'reference' node to a target vertex."""
    refuri = f"{relative_uri}#{target_uid}"
    reference = nodes.reference(refuri=refuri)
    reference.append(nodes.Text(target_uid))
    return reference


class FormatHelper:
    """Helper class for formatting a Vertex."""

    def __init__(
        self,
        uid: str,
        content: nodes.Node,
        parents: Iterable[tuple[str, str]],
        children: Iterable[tuple[str, str]],
    ) -> None:
        """Construct a new FormatHelper.

        Args:
            uid: the unique identifier of the vertex
            content: the nested content of the vertex
            parents: a list of references to parent Vertices
            children: a list of references to child Vertices
        """
        self.uid = uid
        self.content = content
        self.parents = [
            create_reference(uri, target_uid) for (uri, target_uid) in parents
        ]
        self.children = [
            create_reference(uri, target_uid) for (uri, target_uid) in children
        ]

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


def default(helper: FormatHelper) -> nodes.Node:
    """Format a vertex Node as a docutils node."""
    new_content = nodes.Element()
    new_content.append(nodes.Text(f"---start vertex {helper.uid}---"))
    new_content.append(helper.content)
    new_content.append(
        nodes.line(f"---end vertex {helper.uid}---", f"---end vertex {helper.uid}---")
    )
    return new_content


def transparent(helper: FormatHelper) -> nodes.Node:
    """Format a vertex Node as a docutils node."""
    return helper.content


def subtle(helper: FormatHelper) -> nodes.Node:
    """Format a vertex Node as a docutils node using a 'subtle' layout.

    This layout attempts to include all the vertex info, but minimise the impact
    on the layout of the document.
    """
    one_liner = nodes.subscript()

    one_liner += nodes.Text(helper.uid)

    if helper.parents:
        one_liner += nodes.Text(" | ")
        one_liner.extend(helper.parent_list())

    if helper.children:
        one_liner += nodes.Text(" | ")
        one_liner.extend(helper.child_list())

    paragraph = nodes.paragraph()
    paragraph.append(one_liner)

    element = nodes.Element()
    element.append(paragraph)
    element.append(helper.content)

    return element


Formatter = Callable[[FormatHelper], nodes.Node]


LAYOUTS: dict[str, Formatter] = {
    "default": default,
    "transparent": transparent,
    "subtle": subtle,
}


def apply_formatting(
    uid: str,
    content: nodes.Node,
    parents: Iterable[tuple[str, str]],
    children: Iterable[tuple[str, str]],
    layout: str | None,
) -> nodes.Node:
    """Apply a given layout to a Vertex node."""
    if layout is None:
        layout = DEFAULT
    elif layout not in LAYOUTS:
        logger.error(
            f"vertex {uid} has unknown layout '{layout}'. Defaulting to '{DEFAULT}' layout."
        )
        layout = DEFAULT
    helper = FormatHelper(uid, content, parents, children)
    formatter = LAYOUTS[layout]
    return formatter(helper)
