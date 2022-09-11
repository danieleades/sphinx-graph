from dataclasses import dataclass
from typing import List
from docutils import nodes

from sphinx_graph.directives.vertex.node import Node


@dataclass
class Info:
    """Vertex information dataclass."""

    docname: str
    lineno: int
    node: Node
    target: nodes.target
    parents: List[str]
