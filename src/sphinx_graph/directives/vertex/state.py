"""Shared state for the sphinx-graph extension."""

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Dict, Iterator

from docutils import nodes
from networkx import DiGraph
from sphinx.builders import Builder
from sphinx.environment import BuildEnvironment
from sphinx.errors import DocumentError
from sphinx.util import logging

from sphinx_graph.directives.vertex.info import Info as VertexInfo


class DuplicateIdError(DocumentError):
    """Raised when a vertex with the same ID is added to the graph twice."""

    category = "Document Error"


@dataclass
class State:
    """State object for Sphinx Graph vertices."""

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
                print(vertex_info)
                print(f"FINGERPRINT: {parent.fingerprint}")
                self.graph.add_edge(uid, parent.uid, fingerprint=parent.fingerprint)

    def check_fingerprints(self, fingerprints_required: bool) -> None:
        """Check for suspect links and raise sphinx warnings."""
        logger = logging.getLogger(__name__)
        for (child_id, parent_id, fingerprint) in self.graph.edges.data("fingerprint"):
            print(f"FINGERPRINT: {fingerprint}")
            parent = self.all_vertices[parent_id]
            if fingerprints_required and fingerprint is None:
                logger.warning(
                    f"link fingerprints are required, but {child_id} doesn't have a fingerprint for its parent, {parent_id}"
                    f"{parent_id}'s fingerprint is {parent.fingerprint}"
                )
            if fingerprint and fingerprint != parent.fingerprint:
                logger.warning(
                    f"suspect link found. vertex {child_id} is linked to vertex {parent_id} with a fingerprint of {fingerprint},"
                    " but {parent_id}'s fingerprint is {parent.fingerprint}"
                )

    def create_reference(
        self, builder: Builder, target_id: str, from_docname: str
    ) -> nodes.reference:
        """Create a relative reference to a vertex by ID."""
        to_docname = self.all_vertices[target_id].docname
        relative_uri = builder.get_relative_uri(from_docname, to_docname)
        refuri = f"{relative_uri}#{target_id}"
        return nodes.reference(refuri=refuri)


@contextmanager
def get_state(env: BuildEnvironment) -> Iterator[State]:
    """Get the GraphContext object for the given environment."""
    all_vertices = getattr(env, "graph_all_vertices", {})
    graph = getattr(env, "graph_graph", DiGraph())
    state = State(all_vertices, graph)
    yield state
    env.graph_all_vertices = state.all_vertices  # type: ignore[attr-defined]
    env.graph_graph = state.graph  # type: ignore[attr-defined]
