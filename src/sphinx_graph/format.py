"""Helper functions for formating vertices into docutils nodes."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from docutils import nodes

if TYPE_CHECKING:
    from collections.abc import Iterable

T = TypeVar("T")

__all__ = [
    "comma_separated_list",
]


def intersperse(iterable: Iterable[T], delimiter: T) -> Iterable[T]:
    """Intersperse objects in an iterator with another value of the same type."""
    for i, item in enumerate(iterable):
        if i != 0:
            yield delimiter
        yield item


def comma_separated_list(items: Iterable[nodes.Node]) -> Iterable[nodes.Node]:
    """Convert a sequence of docutils nodes into a comma separated list."""
    yield from intersperse(items, nodes.Text(", "))
