"""Queries used to filter and sort vertices for display."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Callable

from sphinx_graph.vertex.state import State

Query = Callable[[State], Iterable[str]]


def noop(state: State) -> Iterable[str]:
    """Simply returns all vertices, in the same order as they arrive."""
    return state.vertices.keys()


QUERIES: dict[str, Query] = {
    "noop": noop,
}


DEFAULT_QUERY = "noop"
