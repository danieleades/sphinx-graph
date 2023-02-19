from __future__ import annotations

from typing import Iterable, TypeVar

from docutils import nodes

T = TypeVar("T")

__all__ = [
    "reference_list",
]


def create_reference(target_uid: str, relative_uri: str) -> nodes.reference:
    """Create a docutils 'reference' node to a target vertex."""
    refuri = f"{relative_uri}#{target_uid}"
    reference = nodes.reference(refuri=refuri)
    reference.append(nodes.Text(target_uid))
    return reference


def intersperse(iterable: Iterable[T], delimiter: T) -> Iterable[T]:
    """Intersperse objects in an iterator with another value of the same type."""
    for i, item in enumerate(iterable):
        if i != 0:
            yield delimiter
        yield item


def comma_separated_list(items: Iterable[nodes.Node]) -> Iterable[nodes.Node]:
    """Convert a sequence of docutils nodes into a comma separated list."""
    yield from intersperse(items, nodes.Text(", "))


def reference_list(references: Iterable[tuple[str, str]]) -> Iterable[nodes.Node]:
    return comma_separated_list(
        create_reference(target_uid, relative_uri)
        for (target_uid, relative_uri) in references
    )
