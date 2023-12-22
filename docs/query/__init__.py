"""Filter and sort vertices for display."""

from __future__ import annotations

from typing import Iterable

import rustworkx as rx

from sphinx_graph.vertex import State


def ancestors(state: State, *, uid: str, include_self: bool = False) -> Iterable[str]:
    """Recursively find all direct parents and descendants of the given node."""
    ancestors: set[str] = set()
    if include_self:
        ancestors.add(uid)

    node_id = state.node_ids[uid]
    ancestors.update(rx.ancestors(state.graph, node_id))

    return ancestors


def descendants(state: State, *, uid: str, include_self: bool = False) -> Iterable[str]:
    """Recursively find all direct parents and descendants of the given node."""
    descendants: set[str] = set()
    if include_self:
        descendants.add(uid)

    node_id = state.node_ids[uid]
    descendants.update(rx.descendants(state.graph, node_id))

    return descendants
