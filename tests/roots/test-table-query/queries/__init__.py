from __future__ import annotations

from typing import Iterable

import rustworkx as rx

from sphinx_graph.vertex import State


def family(state: State, *, uid: str, include_self: bool = False) -> Iterable[str]:
    """Recursively find all direct parents and descendants of the given node."""
    if include_self:
        yield uid

    node_id = state.node_ids[uid]
    yield from (
        state.graph[anc_node_id] for anc_node_id in rx.ancestors(state.graph, node_id)
    )
    yield from (
        state.graph[desc_node_id]
        for desc_node_id in rx.descendants(state.graph, node_id)
    )
