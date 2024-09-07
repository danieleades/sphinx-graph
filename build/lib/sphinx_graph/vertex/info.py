"""Dataclass objects will store information about a Vertex directive."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

    from docutils import nodes

    from sphinx_graph.vertex.config import Config


@dataclass
class Info:
    """Vertex information dataclass.

    Args:
        docname: The name of the current sphinx document
            used for generating interdoc links
        config: Additional configuration for a Vertex
        parents: A mapping from any parent vertices to their last known fingerprint,
            if any
        fingerprint: the 'fingerprint' of this Vertex
            effectively a hash of the Vertices contents
        tags: User-defined tags added to a vertex
    """

    docname: str
    config: Config
    parents: dict[str, str | None]
    fingerprint: str
    tags: list[str]


@dataclass
class InfoParsed:
    """Information about a vertex which is available after parsing the graph."""

    content: nodes.Node
    parents: Iterable[nodes.reference]
    children: Iterable[nodes.reference]
    tags: list[str]
