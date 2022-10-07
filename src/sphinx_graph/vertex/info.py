"""Dataclass objects will store information about a Vertex directive."""
from __future__ import annotations

from dataclasses import dataclass

from docutils import nodes

from sphinx_graph.vertex.node import Node


@dataclass
class Link:
    """A link to another vertex.

    If set, the 'fingerprint' is a hash of the other vertices contents,
    used for enforcing cascading reviews of child vertices after edits.
    """

    uid: str
    fingerprint: str | None


@dataclass
class Info:
    """Vertex information dataclass."""

    docname: str
    lineno: int
    node: Node
    target: nodes.target
    parents: list[Link]
    fingerprint: str
    layout: str


@dataclass
class InfoParsed(Info):
    """Vertex information available after building the entire graph."""

    uid: str
    children: list[str]

    @classmethod
    def from_info(cls, uid: str, info: Info, children: list[str]) -> InfoParsed:
        """Convert an Info object into an InfoParsed object."""
        return cls(
            uid=uid,
            docname=info.docname,
            lineno=info.lineno,
            node=info.node,
            target=info.target,
            parents=info.parents,
            children=children,
            fingerprint=info.fingerprint,
            layout=info.layout,
        )