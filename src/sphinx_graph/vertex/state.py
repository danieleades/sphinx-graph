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

from sphinx_graph.vertex.info import Info

logger = logging.getLogger(__name__)

__all__ = [
    "State",
]


class DuplicateIdError(DocumentError):
    """Raised when a vertex with the same ID is added to the graph twice."""

    category = "Document Error"


@dataclass
class State:
    """State object for Sphinx Graph vertices."""

    vertices: dict[str, Info]
    graph: DiGraph[str]

    def insert(self, uid: str, info: Info) -> None:
        """Insert a vertex into the context.

        Raises:
            DuplicateIdError: If the vertex already exists.
        """
        if uid in self.vertices:
            err_msg = f"Vertex {uid} already exists."
            raise DuplicateIdError(err_msg)
        self.vertices[uid] = info

    @classmethod
    @contextmanager
    def get(cls, env: BuildEnvironment) -> Iterator[State]:
        """Get the State object for the given environment.

        The state is mutable, and changes will be persisted.
        """
        state = cls.read(env)
        yield state
        env.graph_vertices = state.vertices  # type: ignore[attr-defined]
        env.graph_graph = state.graph  # type: ignore[attr-defined]

    @classmethod
    def read(cls, env: BuildEnvironment) -> State:
        """Read the State object for the given environment.

        This is a read-only view of the state. Changes will not be saved.
        """
        vertices = getattr(env, "graph_vertices", {})
        graph: DiGraph[str] = getattr(env, "graph_graph", DiGraph())
        return State(vertices, graph)

    def build_and_check_graph(self) -> None:
        """Build the graph from the list of vertices.

        Also checks the graph for consistency.
        """
        graph = build_graph(self.vertices)
        check_fingerprints(graph, self.vertices)
        check_cycles(graph)
        self.graph = graph


def build_graph(vertices: dict[str, Info]) -> DiGraph[str]:
    """Build the graph from the list of vertices.

    This is called during setup, and doesn't need to be called again.
    """
    graph: DiGraph[str] = DiGraph()
    for uid, vertex_info in vertices.items():
        # add each node
        graph.add_node(uid)

        # add all 'parent' edges
        for parent_uid, fingerprint in vertex_info.parents.items():
            graph.add_edge(parent_uid, uid, fingerprint=fingerprint)
    return graph


def check_fingerprints(graph: DiGraph[str], vertices: dict[str, Info]) -> None:
    """Check for suspect links and raise sphinx warnings."""
    fingerprint: str | None
    for parent_id, child_id, fingerprint in graph.edges.data("fingerprint"):
        fingerprints_required = vertices[child_id].config.require_fingerprints
        parent = vertices[parent_id]
        if fingerprints_required and fingerprint is None:
            logger.warning(
                f"link fingerprints are required, but {child_id} doesn't have a"
                f" fingerprint for its link to its parent {parent_id}.\nthe fingerprint"
                f" can be added by changing the parent reference on {child_id} to"
                f" '{parent_id}:{parent.fingerprint}'.",
            )
        if fingerprint and fingerprint != parent.fingerprint:
            logger.warning(
                f"suspect link found. vertex {child_id} is linked to vertex"
                f" {parent_id} with a fingerprint of '{fingerprint}', but {parent_id}'s"
                f" fingerprint is '{parent.fingerprint}'.\n{child_id} should be"
                " reviewed, and the link fingerprint manually updated.",
            )


def check_cycles(graph: DiGraph[str]) -> None:
    """Ensure there are no dependency cycles in the graph."""
    for cycle in simple_cycles(graph):
        logger.error(
            f"vertices must not have cyclic dependencies. cycle detected: {cycle}",
        )
