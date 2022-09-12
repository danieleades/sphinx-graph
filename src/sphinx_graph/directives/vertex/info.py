from dataclasses import asdict, dataclass
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


@dataclass
class InfoParsed:
    """Vertex information available after building the entire graph."""

    id: str
    docname: str
    lineno: int
    node: Node
    target: nodes.target
    parents: List[str]
    children: List[str]

    @classmethod
    def from_info(cls, id: str, children: list[str], info: Info) -> "InfoParsed":
        return cls(id=id, children=children, **asdict(info))
