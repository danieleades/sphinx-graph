from typing import Callable, Iterable

from sphinx_graph.vertex.state import State

Query = Callable[[State], Iterable[str]]


def noop(state: State) -> Iterable[str]:
    return state.vertices.keys()


QUERIES: dict[str, Query] = {
    "noop": noop,
}


DEFAULT_QUERY = "noop"
