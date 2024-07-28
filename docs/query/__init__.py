"""Filter and sort vertices for display."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sphinx_graph.vertex.query import query_wrapper

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sphinx_graph.vertex import State


@query_wrapper
def ancestors(state: State, *, uid: str, include_self: bool = False) -> Iterable[str]:
    """Recursively find all direct parents and ancestors of the given node."""
    if include_self:
        yield uid
    yield from state.ancestors(uid)


@query_wrapper
def descendants(state: State, *, uid: str, include_self: bool = False) -> Iterable[str]:
    """Recursively find all direct children and descendants of the given node."""
    if include_self:
        yield uid
    yield from state.descendants(uid)
