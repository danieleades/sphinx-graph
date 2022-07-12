"""Vertex information dataclass."""

from dataclasses import dataclass

from docutils import nodes

from sphinx_graph.vertex.node import Vertex


@dataclass
class VertexInfo:
    """Vertex information dataclass."""

    id: str
    docname: str
    lineno: int
    vertex: Vertex
    target: nodes.target
