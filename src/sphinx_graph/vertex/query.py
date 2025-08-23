"""Queries used to filter and sort vertices for display."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING, Concatenate, ParamSpec

if TYPE_CHECKING:
    from sphinx_graph.vertex.state import State

P = ParamSpec("P")

# Enforce that the first positional parameter is a `State`, while allowing
# arbitrary additional positional/keyword parameters via `ParamSpec`.
Query = Callable[Concatenate["State", P], Iterable[str]]


def noop(state: State) -> Iterable[str]:
    """Simply returns all vertices, in the same order as they arrive."""
    return state.vertices.keys()


QUERIES: dict[str, Query] = {
    "noop": noop,
}


DEFAULT_QUERY = "noop"
