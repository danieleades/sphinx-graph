"""Shared state for the sphinx-graph extension."""

from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Dict, Iterator

from sphinx.environment import BuildEnvironment
from sphinx.errors import DocumentError

from sphinx_graph.vertex.info import VertexInfo


class DuplicateIdError(DocumentError):
    """Raised when a vertex with the same ID is added to the graph twice."""

    category = "Document Error"


@dataclass
class GraphContext:
    """Context object for Sphinx Graph."""

    all_vertices: Dict[str, VertexInfo] = field(default_factory=dict)

    def insert_vertex(self, vertex_info: VertexInfo) -> None:
        """Insert a vertex into the context.

        Raises:
            DuplicateIdError: If the vertex already exists.
        """
        if vertex_info.id in self.all_vertices:
            raise DuplicateIdError(f"Vertex {vertex_info.id} already exists.")
        self.all_vertices[vertex_info.id] = vertex_info


@contextmanager
def get_context(env: BuildEnvironment) -> Iterator[GraphContext]:
    """Get the GraphContext object for the given environment."""
    all_vertices = getattr(env, "graph_all_vertices", {})
    context = GraphContext(all_vertices)
    yield context
    env.graph_all_vertices = context.all_vertices  # type: ignore[attr-defined]
