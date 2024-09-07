"""Shared state for the sphinx-graph extension."""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping
from contextlib import contextmanager
from typing import TYPE_CHECKING

import rustworkx as rx
from sphinx.errors import DocumentError
from sphinx.util import logging

from sphinx_graph.vertex.info import Info

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment

logger = logging.getLogger(__name__)

__all__ = [
    "State",
]


class DuplicateIdError(DocumentError):
    """Raised when a vertex with the same ID is added to the graph twice."""

    category = "Document Error"


@contextmanager
def _vertices_tmp(env: BuildEnvironment) -> Iterator[dict[str, Info]]:
    vertices: dict[str, Info] = getattr(env, "graph_vertices_tmp", {})
    yield vertices
    env.graph_vertices_tmp = vertices  # type: ignore[attr-defined]


def purge(_app: Sphinx, env: BuildEnvironment, docname: str) -> None:
    """Clear out all stale vertices.

    All vertices whose docname matches the given one from the graph_all_vertices list
    will be removed.

    If there are vertices left in the document, they will be added again during parsing.
    """
    with _vertices_tmp(env) as vertices:
        vertices = {  # noqa: PLW2901
            uid: vert for uid, vert in vertices.items() if vert.docname != docname
        }


def merge(
    _app: Sphinx,
    env: BuildEnvironment,
    _docnames: list[str],
    other: BuildEnvironment,
) -> None:
    """Merge the vertices from multiple environments during parallel builds."""
    with _vertices_tmp(env) as vertices, _vertices_tmp(other) as other_vertices:
        vertices.update(other_vertices)


def insert_vertex(env: BuildEnvironment, uid: str, info: Info) -> None:
    """Insert a vertex into the build environment."""
    with _vertices_tmp(env) as vertices:
        if uid in vertices:
            err_msg = f"Vertex {uid} already exists."
            raise DuplicateIdError(err_msg)
        vertices[uid] = info


def build_and_check_graph(env: BuildEnvironment) -> State:
    """Build the graph from the collected vertices.

    Also checks the graph for consistency.
    """
    vertices_tmp: dict[str, Info] = env.graph_vertices_tmp  # type: ignore[attr-defined]
    vertices: dict[str, tuple[int, Info]] = {}
    graph: rx.PyDiGraph[str, str | None] = rx.PyDiGraph()

    for uid, info in vertices_tmp.items():
        node_id = graph.add_node(uid)
        vertices[uid] = node_id, info

    build_graph_edges(vertices, graph)

    env.graph_vertices = vertices  # type: ignore[attr-defined]
    env.graph_graph = graph  # type: ignore[attr-defined]

    return State(vertices, graph)


class State:
    """State object for Sphinx Graph vertices."""

    def __init__(
        self,
        vertices: dict[str, tuple[int, Info]],
        graph: rx.PyDiGraph[str, str | None],
    ) -> None:
        """Create a new state object."""
        self._vertices = vertices
        self._graph = graph

    @classmethod
    def read(cls, env: BuildEnvironment) -> State:
        """Read the State object for the given environment.

        This is a read-only view of the state. Changes will not be saved.
        """
        vertices = getattr(env, "graph_vertices", {})
        graph: rx.PyDiGraph[str, str | None] = getattr(
            env, "graph_graph", rx.PyDiGraph(multigraph=False)
        )
        return State(vertices, graph)

    @property
    def graph(self) -> rx.PyDiGraph[str, str | None]:
        """A graph representing the relationships between vertices.

        Vertices in the graph are stored using 'node ids'. These can be retrieved using
        the `State.node_ids` mapping.
        """
        return self._graph

    @property
    def vertices(self) -> Mapping[str, Info]:
        """A mapping from vertex uid to vertex Info."""
        return Vertices(self._vertices)

    @property
    def node_ids(self) -> Mapping[str, int]:
        """A mapping from vertex uid to graph node ID."""
        return NodeIds(self._vertices)

    def children(self, uid: str) -> Iterable[str]:
        """Iterate over the children of the given node."""
        node_id, _info = self._vertices[uid]
        yield from self._graph.successors(node_id)

    def ancestors(self, uid: str) -> Iterable[str]:
        """Recursively find all direct parents and ancestors of the given node."""
        node_id = self.node_ids[uid]
        yield from (
            self.graph[anc_node_id] for anc_node_id in rx.ancestors(self.graph, node_id)
        )

    def descendants(self, uid: str) -> Iterable[str]:
        """Recursively find all direct children and descendants of the given node."""
        node_id = self.node_ids[uid]
        yield from (
            self.graph[desc_node_id]
            for desc_node_id in rx.descendants(self.graph, node_id)
        )


class Vertices(Mapping[str, Info]):
    """A dict-like view of vertex Info keyed by vertex ID."""

    def __init__(self, vertices: dict[str, tuple[int, Info]]) -> None:
        self._vertices = vertices

    def __getitem__(self, key: str) -> Info:
        _node_id, info = self._vertices[key]
        return info

    def __iter__(self) -> Iterator[str]:
        return iter(self._vertices)

    def __len__(self) -> int:
        return len(self._vertices)


class NodeIds(Mapping[str, int]):
    """A dict-like view of graph node IDs keyed by vertex ID."""

    def __init__(self, vertices: dict[str, tuple[int, Info]]) -> None:
        self._vertices = vertices

    def __getitem__(self, key: str) -> int:
        node_id, _info = self._vertices[key]
        return node_id

    def __iter__(self) -> Iterator[str]:
        return iter(self._vertices)

    def __len__(self) -> int:
        return len(self._vertices)


def build_graph_edges(
    vertices: Mapping[str, tuple[int, Info]], graph: rx.PyDiGraph[str, str | None]
) -> None:
    """Build the graph from the list of vertices.

    This is called during setup, and doesn't need to be called again.
    """
    # add all 'parent' edges
    for uid, (node_id, info) in vertices.items():
        fingerprints_required = info.config.require_fingerprints
        for parent_uid, fingerprint in info.parents.items():
            try:
                parent_node_id, parent = vertices[parent_uid]
            except KeyError:
                logger.exception(
                    f"vertex '{uid}' has a parent link to '{parent_uid}',"
                    f" but '{parent_uid}' doesn't exist"
                )
            if fingerprints_required and fingerprint is None:
                logger.warning(
                    f"link fingerprints are required, but {uid} doesn't have a"
                    f" fingerprint for its link to its parent {parent_uid}.\nthe"
                    f" fingerprint can be added by changing the parent reference on"
                    f" {uid} to '{parent_uid}:{parent.fingerprint}'.",
                )
            if fingerprint and fingerprint != parent.fingerprint:
                logger.warning(
                    f"suspect link found. vertex {uid} is linked to vertex"
                    f" {parent_uid} with a fingerprint of '{fingerprint}', but"
                    f" {parent_uid}'s fingerprint is '{parent.fingerprint}'.\n{uid}"
                    " should be reviewed, and the link fingerprint manually updated.",
                )

            graph.add_edge(parent_node_id, node_id, fingerprint)

    cycles = [
        [graph[node_id] for node_id in node_ids] for node_ids in rx.simple_cycles(graph)
    ]
    if cycles:
        suffix = ", ".join(
            f"[{uids[0]} -> {' -> '.join(uids[1:])} -> {uids[0]}]" for uids in cycles
        )
        logger.exception(
            f"vertices must not have cyclic dependencies. cycles detected: {suffix}"
        )
