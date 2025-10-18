from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sphinx_graph.vertex import State


def siblings(state: State, *, uid: str, include_self: bool = False) -> Iterable[str]:
    """Return the siblings of a vertex, optionally including the vertex itself."""
    parents = state.vertices[uid].parents
    for parent in parents:
        for child in state.children(parent):
            if include_self or child != uid:
                yield child
