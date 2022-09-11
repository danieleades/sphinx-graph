"""Shared state for the sphinx-graph extension."""

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Dict, Iterator

from networkx import DiGraph
from sphinx.environment import BuildEnvironment
from sphinx.errors import DocumentError
from sphinx_graph.directives.vertex.info import Info as VertexInfo


class DuplicateIdError(DocumentError):
    """Raised when a vertex with the same ID is added to the graph twice."""

    category = "Document Error"


@dataclass
class Context:
    """Context object for Sphinx Graph."""

    all_vertices: Dict[str, VertexInfo]
    graph: DiGraph

    def insert_vertex(self, uid: str, info: VertexInfo) -> None:
        """Insert a vertex into the context.

        Raises:
            DuplicateIdError: If the vertex already exists.
        """
        if uid in self.all_vertices:
            raise DuplicateIdError(f"Vertex {uid} already exists.")
        self.all_vertices[uid] = info

    def build_graph(self) -> None:
        """Build the graph from the list of vertices.

        This is called during setup, and doesn't need to be called again.
        """
        for uid, vertex_info in self.all_vertices.items():

            # add each node
            self.graph.add_node(uid)

            # add all 'parent' edges
            for parent in vertex_info.parents:
                self.graph.add_edge(uid, parent)


@contextmanager
def get_context(env: BuildEnvironment) -> Iterator[Context]:
    """Get the GraphContext object for the given environment."""
    all_vertices = getattr(env, "graph_all_vertices", {})
    graph = getattr(env, "graph_graph", DiGraph())
    context = Context(all_vertices, graph)
    yield context
    env.graph_all_vertices = context.all_vertices  # type: ignore[attr-defined]
    env.graph_graph = context.graph  # type: ignore[attr-defined]
