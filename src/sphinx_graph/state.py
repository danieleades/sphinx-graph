"""Shared state for the sphinx-graph extension."""

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Dict, Iterator

from sphinx.environment import BuildEnvironment
from sphinx.errors import DocumentError
from sphinx.util import logging

from sphinx_graph.info import Info as VertexInfo

logger = logging.getLogger(__name__)


class DuplicateIdError(DocumentError):
    """Raised when a vertex with the same ID is added to the graph twice."""

    category = "Document Error"


@dataclass
class State:
    """State object for Sphinx Graph vertices."""

    all_vertices: Dict[str, VertexInfo]

    def insert_vertex(self, uid: str, info: VertexInfo) -> None:
        """Insert a vertex into the context.

        Raises:
            DuplicateIdError: If the vertex already exists.
        """
        if uid in self.all_vertices:
            raise DuplicateIdError(f"Vertex {uid} already exists.")
        self.all_vertices[uid] = info

    @classmethod
    @contextmanager
    def get(cls, env: BuildEnvironment) -> Iterator["State"]:
        """Get the GraphContext object for the given environment."""
        all_vertices = getattr(env, "graph_all_vertices", {})
        state = State(all_vertices)
        yield state
        env.graph_all_vertices = state.all_vertices  # type: ignore[attr-defined]


@contextmanager
def get_state(env: BuildEnvironment) -> Iterator[State]:
    """Get the GraphContext object for the given environment."""
    all_vertices = getattr(env, "graph_all_vertices", {})
    state = State(all_vertices)
    yield state
    env.graph_all_vertices = state.all_vertices  # type: ignore[attr-defined]
