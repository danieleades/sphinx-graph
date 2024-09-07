"""Shared state for the sphinx-graph extension."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING

from sphinx.util import logging

from sphinx_graph.vertex.state import DuplicateIdError

if TYPE_CHECKING:
    from collections.abc import Iterator
    from uuid import UUID

    from sphinx.environment import BuildEnvironment

    from sphinx_graph import table
    from sphinx_graph.table.info import Info

logger = logging.getLogger(__name__)

__all__ = [
    "State",
]


@dataclass
class State:
    """State object for Sphinx Graph vertex tables."""

    tables: dict[UUID, table.Info]

    def insert(self, uid: UUID, info: Info) -> None:
        """Insert a vertex into the context.

        Raises:
            DuplicateIdError: If the vertex already exists.
        """
        if uid in self.tables:
            err_msg = f"Vertex table {uid} already exists."
            raise DuplicateIdError(err_msg)
        self.tables[uid] = info

    @classmethod
    def read(cls, env: BuildEnvironment) -> State:
        """Get the State object for the given environment."""
        tables = getattr(env, "graph_tables", {})
        return State(tables)

    @classmethod
    @contextmanager
    def get(cls, env: BuildEnvironment) -> Iterator[State]:
        """Get the State object for the given environment."""
        state = cls.read(env)
        yield state
        env.graph_tables = state.tables  # type: ignore[attr-defined]
