"""Vertex information dataclass."""

from dataclasses import dataclass
from typing import List

from docutils import nodes

from sphinx_graph.vertex.node import Vertex


@dataclass
class VertexInfo:
    """Vertex information dataclass."""

    docname: str
    lineno: int
    node: Vertex
    target: nodes.target
    parents: List[str]
    children: List[str]
