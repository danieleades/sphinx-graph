from typing import Iterable

import networkx as nx

from sphinx_graph.vertex import State


def ancestors(state: State, *, uid: str, include_self: bool = False) -> Iterable[str]:
    """Recursively find all direct parents and descendents of the given node"""
    ancestors: set[str] = set()
    if include_self:
        ancestors.add(uid)

    ancestors.update(nx.ancestors(state.graph, uid))

    return ancestors


def descendants(state: State, *, uid: str, include_self: bool = False) -> Iterable[str]:
    """Recursively find all direct parents and descendents of the given node"""
    descendants: set[str] = set()
    if include_self:
        descendants.add(uid)

    descendants.update(nx.descendants(state.graph, uid))

    return descendants
