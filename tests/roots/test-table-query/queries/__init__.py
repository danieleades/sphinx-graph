from __future__ import annotations

from typing import Iterable

import networkx as nx

from sphinx_graph.vertex import State


def family(state: State, *, uid: str, include_self: bool = False) -> Iterable[str]:
    """Recursively find all direct parents and descendants of the given node."""
    family: set[str] = set()
    if include_self:
        family.add(uid)

    family.update(nx.ancestors(state.graph, uid))
    family.update(nx.descendants(state.graph, uid))

    return family
