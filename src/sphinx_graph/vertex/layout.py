"""Tools and methods for formatting vertex nodes into docutils nodes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, TypeVar

from docutils import nodes
from sphinx.util import logging

from sphinx_graph.format import reference_list

logger = logging.getLogger(__name__)

__all__ = [
    "FormatHelper",
    "Formatter",
    "LAYOUTS",
    "DEFAULT",
]

DEFAULT = "subtle"


T = TypeVar("T")


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
    parents: Iterable[tuple[str, str]]
    children: Iterable[tuple[str, str]]

    def _list(
        self, references: Iterable[tuple[str, str]], prefix: str | None
    ) -> nodes.line | None:
        refs = list(reference_list(references))
        if not refs:
            return None

        line = nodes.line()
        if prefix:
            line += nodes.Text(prefix)
        line.extend(refs)

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

    parents = helper.parent_list()
    if parents:
        one_liner += nodes.Text(" | ")
        one_liner.extend(parents)

    children = helper.child_list()
    if children:
        one_liner += nodes.Text(" | ")
        one_liner.extend(children)

    paragraph = nodes.paragraph()
    paragraph.append(one_liner)

    element = nodes.Element()
    element.append(paragraph)
    element.append(helper.content)

    return element


Formatter = Callable[[FormatHelper], nodes.Node]


LAYOUTS: dict[str, Formatter] = {
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
            f"vertex {uid} has unknown layout '{layout}'. Defaulting to '{DEFAULT}'"
            " layout."
        )
        layout = DEFAULT
    helper = FormatHelper(uid, content, list(parents), list(children))
    formatter = LAYOUTS[layout]
    return formatter(helper)
