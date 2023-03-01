"""Shared state for the sphinx-graph extension."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterator

from networkx import DiGraph
from networkx.algorithms.cycles import simple_cycles
from sphinx.environment import BuildEnvironment
from sphinx.errors import DocumentError
from sphinx.util import logging

from sphinx_graph.info import Info as VertexInfo

logger = logging.getLogger(__name__)

__all__ = [
    "State",
    "build_and_check_graph",
]


class DuplicateIdError(DocumentError):
    """Raised when a vertex with the same ID is added to the graph twice."""

    category = "Document Error"


@dataclass
class State:
    """State object for Sphinx Graph vertices."""

    all_vertices: dict[str, VertexInfo]

    def insert_vertex(self, uid: str, info: VertexInfo) -> None:
        """Insert a vertex into the context.

        Raises:
            DuplicateIdError: If the vertex already exists.
        """
        if uid in self.all_vertices:
            err_msg = f"Vertex {uid} already exists."
            raise DuplicateIdError(err_msg)
        self.all_vertices[uid] = info

    @classmethod
    @contextmanager
    def get(cls, env: BuildEnvironment) -> Iterator[State]:
        """Get the GraphContext object for the given environment."""
        all_vertices = getattr(env, "graph_all_vertices", {})
        state = cls(all_vertices)
        yield state
        env.graph_all_vertices = state.all_vertices  # type: ignore[attr-defined]


def build_graph(vertices: dict[str, VertexInfo]) -> DiGraph:
    """Build the graph from the list of vertices.

    This is called during setup, and doesn't need to be called again.
    """
    graph = DiGraph()
    for uid, vertex_info in vertices.items():
        # add each node
        graph.add_node(uid)

        # add all 'parent' edges
        for parent_uid, fingerprint in vertex_info.parents.items():
            graph.add_edge(uid, parent_uid, fingerprint=fingerprint)
    return graph


def check_fingerprints(graph: DiGraph, vertices: dict[str, VertexInfo]) -> None:
    """Check for suspect links and raise sphinx warnings."""
    for child_id, parent_id, fingerprint in graph.edges.data("fingerprint"):
        fingerprints_required = vertices[child_id].config.require_fingerprints
        parent = vertices[parent_id]
        if fingerprints_required and fingerprint is None:
            logger.warning(
                f"link fingerprints are required, but {child_id} doesn't have a"
                f" fingerprint for its link to its parent {parent_id}.\nthe fingerprint"
                f" can be added by changing the parent reference on {child_id} to"
                f" '{parent_id}:{parent.fingerprint}'."
            )
        if fingerprint and fingerprint != parent.fingerprint:
            logger.warning(
                f"suspect link found. vertex {child_id} is linked to vertex"
                f" {parent_id} with a fingerprint of '{fingerprint}', but {parent_id}'s"
                f" fingerprint is '{parent.fingerprint}'.\n{child_id} should be"
                " reviewed, and the link fingerprint manually updated."
            )


def check_cycles(graph: DiGraph) -> None:
    """Ensure there are no dependency cycles in the graph."""
    for cycle in simple_cycles(graph):
        logger.error(
            f"vertices must not have cyclic dependencies. cycle detected: {cycle}"
        )


def build_and_check_graph(vertices: dict[str, VertexInfo]) -> DiGraph:
    """Build the graph from the list of vertices.

    Also checks the graph for consistency.
    """
    graph = build_graph(vertices)
    check_fingerprints(graph, vertices)
    check_cycles(graph)
    return graph
