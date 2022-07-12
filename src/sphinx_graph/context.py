"""Shared state for the sphinx-graph extension."""

from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Iterator, List

from sphinx.environment import BuildEnvironment

from sphinx_graph.vertex.info import VertexInfo


@dataclass
class GraphContext:
    """Context object for Sphinx Graph."""

    all_vertices: List[VertexInfo] = field(default_factory=list)


@contextmanager
def get_context(env: BuildEnvironment) -> Iterator[GraphContext]:
    """Get the GraphContext object for the given environment."""
    all_vertices = getattr(env, "graph_all_vertices", [])
    context = GraphContext(all_vertices)
    yield context
    env.graph_all_vertices = context.all_vertices  # type: ignore[attr-defined]
