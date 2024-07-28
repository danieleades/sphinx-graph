"""Queries used to filter and sort vertices for display."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from functools import wraps
from typing import Any, Concatenate, ParamSpec, Protocol

from sphinx_graph.vertex.state import State

P = ParamSpec("P")


class QueryBase(Protocol[P]):
    def __call__(self, state: State, **kwargs: P.kwargs) -> Iterable[str]: ...


Query = QueryBase[Any]


def query_wrapper(func: Callable[Concatenate[State, P], Iterable[str]]) -> Query:
    @wraps(func)
    def wrapper(state: State, **kwargs: Any) -> Iterable[str]:
        return func(state, **kwargs)

    return wrapper


def noop(state: State, **_kwargs: Any) -> Iterable[str]:
    """Simply returns all vertices, in the same order as they arrive."""
    return state.vertices.keys()


QUERIES: dict[str, Query] = {
    "noop": noop,
}


DEFAULT_QUERY = "noop"
