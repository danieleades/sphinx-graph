"""Utility methods for SphinxGraph."""

from typing import Iterable, Optional, TypeVar

from docutils import nodes

T = TypeVar("T")


def unwrap(x: Optional[T]) -> T:
    """Unwrap an optional value.

    Args:
        x: The optional value to unwrap.

    Returns:
        The unwrapped value.

    Raises:
        ValueError: If the value is None.
    """
    if x is None:
        raise ValueError("attempted to 'unwrap' a None value!")
    return x


def intersperse(iterable: Iterable[T], delimiter: T) -> Iterable[T]:
    """Intersperse objects in an iterator with another value of the same type."""
    for i, item in enumerate(iterable):
        if i != 0:
            yield delimiter
        yield item


def comma_separated_list(items: Iterable[nodes.Node]) -> Iterable[nodes.Node]:
    """Convert a sequence of docutils nodes into a comma separated list."""
    yield from intersperse(items, nodes.Text(", "))
