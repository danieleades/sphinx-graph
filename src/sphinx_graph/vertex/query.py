"""Queries used to filter and sort vertices for display."""

from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any, ParamSpec, Protocol

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from typing import Concatenate

    from sphinx_graph.vertex.state import State

P = ParamSpec("P")


class QueryBase(Protocol[P]):
    def __call__(self, state: State, **kwargs: P.kwargs) -> Iterable[str]: ...


Query = QueryBase[Any]


def query_wrapper(func: Callable[Concatenate[State, P], Iterable[str]]) -> Query:
    @wraps(func)
    def wrapper(state: State, **kwargs: P.kwargs) -> Iterable[str]:
        return func(state, **kwargs)

    return wrapper


@query_wrapper
def noop(state: State) -> Iterable[str]:
    """Simply returns all vertices, in the same order as they arrive."""
    return state.vertices.keys()


QUERIES: dict[str, Query] = {
    "noop": noop,
}


DEFAULT_QUERY = "noop"
