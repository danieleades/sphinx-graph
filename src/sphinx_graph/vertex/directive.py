"""Sphinx Directive for Vertex objects."""

from __future__ import annotations

import base64
import hashlib
from dataclasses import dataclass, field
from typing import Sequence

from docutils import nodes
from sphinx.util.docutils import SphinxDirective

from sphinx_graph.vertex import parse
from sphinx_graph.vertex.info import Info, Link
from sphinx_graph.vertex.layout import DEFAULT_LAYOUT
from sphinx_graph.vertex.node import Node
from sphinx_graph.vertex.state import get_state

__all__ = [
    "Directive",
]


@dataclass
class Args:
    """Parsed arguments for the Vertex directive."""

    uid: str
    parents: list[Link] = field(default_factory=list)
    layout: str = DEFAULT_LAYOUT


class Directive(SphinxDirective):
    """An RST node representing a To-Do item."""

    has_content = True
    required_arguments = 1
    option_spec = {
        "parents": parse.parents,
        "layout": parse.string,
    }

    def run(self) -> Sequence[nodes.Node]:
        """Run the directive and return a Vertex node."""
        args = Args(uid=self.arguments[0], **self.options)

        content_node = Node("\n".join(self.content))
        self.state.nested_parse(self.content, self.content_offset, content_node)

        fingerprint = base64.b64encode(
            hashlib.md5(content_node.astext().encode()).digest()
        )[:4].decode()

        targetnode = nodes.target("", "", ids=[args.uid])
        placeholder_node = Node(graph_uid=args.uid)

        with get_state(self.env) as state:
            state.insert_vertex(
                args.uid,
                Info(
                    docname=self.env.docname,
                    lineno=self.lineno,
                    node=content_node,
                    target=targetnode,
                    parents=args.parents,
                    fingerprint=fingerprint,
                    layout=args.layout,
                ),
            )

        return [targetnode, placeholder_node]
