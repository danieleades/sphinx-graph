"""Vertex information dataclass."""

from dataclasses import dataclass
from typing import List

from docutils import nodes

from sphinx_graph.vertex.node import VertexNode


@dataclass
class VertexInfo:
    """Vertex information dataclass."""

    docname: str
    lineno: int
    node: VertexNode
    target: nodes.target
    parents: List[str]

