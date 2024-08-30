"""Tools and methods for formatting vertex nodes into docutils nodes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, TypeVar

from docutils import nodes
from sphinx.util import logging

from sphinx_graph.formatting import comma_separated_list

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sphinx_graph.vertex.info import InfoParsed

logger = logging.getLogger(__name__)

__all__ = [
    "DEFAULT",
    "LAYOUTS",
    "FormatHelper",
    "Formatter",
]

DEFAULT = "subtle"


T = TypeVar("T")


@dataclass
class FormatHelper:
    """Helper class for formatting a Vertex.

    Args:
        uid: the unique identifier of the vertex
        info: vertex information
    """

    uid: str
    info: InfoParsed

    def child_list(self) -> nodes.line | None:
        """Format the list of child vertex references as a comma-separated list.

        Args:
            prefix: Optionally set a prefix for the list
        """
        return _list(self.info.children)

    def parent_list(self) -> nodes.line | None:
        """Format the list of parent vertex references as a comma-separated list.

        Args:
            prefix: Optionally set a prefix for the list
        """
        return _list(self.info.parents)


def _list(references: Iterable[nodes.reference]) -> nodes.line | None:
    """Format nodes as a comma-separated list."""
    refs = list(comma_separated_list(references))
    if not refs:
        return None

    line = nodes.line()
    line.extend(refs)

    return line


def transparent(helper: FormatHelper) -> nodes.Node:
    """Format a vertex Node as a docutils node."""
    return helper.info.content


def subtle(helper: FormatHelper) -> nodes.Node:
    """Format a vertex Node as a docutils node using a 'subtle' layout."""
    one_liner = nodes.subscript()
    one_liner += nodes.Text(helper.uid)

    def _format_tags(tags: list[str]) -> Iterable[nodes.Node] | None:
        """Format a list of tags as a comma-separated list."""
        if not tags:
            return None
        return comma_separated_list(nodes.Text(tag) for tag in tags)

    # Iterate through labels and their corresponding content
    for label, content in [
        ("Parents", helper.parent_list()),
        ("Children", helper.child_list()),
        ("Tags", _format_tags(helper.info.tags)),
    ]:
        # If content exists for the label, add it to the one_liner
        if content:
            # Add a separator and label
            one_liner += nodes.Text(f" | {label}: ")
            one_liner.extend(content)

    paragraph = nodes.paragraph()
    paragraph.extend([one_liner, helper.info.content])

    return paragraph


Formatter = Callable[[FormatHelper], nodes.Node]


LAYOUTS: dict[str, Formatter] = {
    "transparent": transparent,
    "subtle": subtle,
}


def apply_formatting(
    uid: str,
    info: InfoParsed,
    layout: str | None,
) -> nodes.Node:
    """Apply a given layout to a Vertex node."""
    if layout is None:
        layout = DEFAULT
    elif layout not in LAYOUTS:
        logger.error(
            f"vertex {uid} has unknown layout '{layout}'. Defaulting to '{DEFAULT}'"
            " layout.",
        )
        layout = DEFAULT
    helper = FormatHelper(uid, info)
    formatter = LAYOUTS[layout]
    return formatter(helper)
