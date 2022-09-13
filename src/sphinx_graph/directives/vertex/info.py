"""Dataclass objects will store information about a Vertex directive."""
from __future__ import annotations

from dataclasses import asdict, dataclass

from docutils import nodes

from sphinx_graph.directives.vertex.node import Node


@dataclass
class Info:
    """Vertex information dataclass."""

    docname: str
    lineno: int
    node: Node
    target: nodes.target
    parents: list[str]


@dataclass
class InfoParsed:
    """Vertex information available after building the entire graph."""

    id: str
    docname: str
    lineno: int
    node: Node
    target: nodes.target
    parents: list[str]
    children: list[str]

    @classmethod
    def from_info(cls, id: str, children: list[str], info: Info) -> InfoParsed:
        """Convert an Info object into an InfoParsed object."""
        return cls(id=id, children=children, **asdict(info))
