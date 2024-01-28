from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sphinx_graph.vertex import State


def family(state: State, *, uid: str, include_self: bool = False) -> Iterable[str]:
    """Recursively find all direct parents and descendants of the given node."""
    if include_self:
        yield uid
    yield from state.ancestors(uid)
    yield from state.descendants(uid)
