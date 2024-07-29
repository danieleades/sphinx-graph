"""Queries used to filter and sort vertices for display."""

from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any, ParamSpec, Protocol

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from typing import Concatenate

    from sphinx_graph.vertex.state import State

P = ParamSpec("P")


class Query(Protocol):
    """Protocol defining the structure of query functions.

    A query function takes a State object and optional keyword arguments,
    and returns an iterable of strings representing vertex IDs.
    """

    def __call__(self, state: State, **kwargs: Any) -> Iterable[str]:  # noqa: ANN401
        """Execute the query.

        Args:
            state: The current state of the vertex graph.
            **kwargs: Additional keyword arguments for the query.

        Returns:
            An iterable of vertex IDs resulting from the query.
        """
        ...


def query_wrapper(func: Callable[Concatenate[State, P], Iterable[str]]) -> Query:
    """Decorator to wrap a function to conform to the Query protocol.

    This wrapper ensures that a wrapped function with specific keyword arguments has
    the signature: `(state: State, **kwargs: Any) -> Iterable[str]`

    Args:
        func: The function to wrap.

    Returns:
        A wrapped version of the function conforming to the Query protocol.

    Example:
        # custom_query.py
        @query_wrapper
        def custom_query(state: State, *, filter_type: str = "all") -> Iterable[str]:
            '''Custom query to filter vertices based on a type.'''
            if filter_type == "all":
                return state.vertices.keys()
            return (
                vid for vid, data
                in state.vertices.items()
                if data.get("type") == filter_type
            )

        # ---

        # conf.py
        from .custom_query import custom_query
        graph_config = Config(
            queries={
                "custom_query": custom_query,
            },
        )
    """

    @wraps(func)
    def wrapper(state: State, **kwargs: P.kwargs) -> Iterable[str]:
        """Wrapper function that conforms to the Query protocol.

        Args:
            state: The current state of the vertex graph.
            **kwargs: Additional keyword arguments for the query.

        Returns:
            The result of calling the wrapped function.
        """
        return func(state, **kwargs)

    return wrapper


@query_wrapper
def noop(state: State) -> Iterable[str]:
    """Query that returns all vertices without modification.

    This query simply returns all vertices in the order they appear in the state.

    Args:
        state: The current state of the vertex graph.

    Returns:
        An iterable of all vertex IDs in the state.
    """
    return state.vertices.keys()


QUERIES: dict[str, Query] = {
    "noop": noop,
}
"""Dictionary of available queries, mapping query names to query functions."""


DEFAULT_QUERY = "noop"
"""The default query to use if no specific query is specified."""
