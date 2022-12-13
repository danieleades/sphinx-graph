"""Dataclass objects will store information about a Vertex directive."""
from dataclasses import dataclass

from sphinx_graph.config import VertexConfig


@dataclass
class Info:
    """Vertex information dataclass."""

    docname: str
    config: VertexConfig
    parents: dict[str, str | None]
    fingerprint: str
