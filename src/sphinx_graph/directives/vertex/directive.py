"""Sphinx Directive for Vertex objects."""
from __future__ import annotations

import base64
import hashlib
from dataclasses import dataclass, field
from typing import Sequence

from docutils import nodes
from sphinx.util.docutils import SphinxDirective

from sphinx_graph import parse
from sphinx_graph.directives.vertex.info import Info, Link
from sphinx_graph.directives.vertex.node import Node
from sphinx_graph.directives.vertex.state import get_state
from sphinx_graph.directives.vertex.layout import DEFAULT_FORMATTER

__all__ = [
    "Directive",
]


def parse_parents(input: str | None) -> list[Link]:
    """Parse a comma separated list of parent link specifications.

    each element in the list may be in one of two forms

    - {PARENT_ID}
    - {PARENT_ID}:{PARENT_FINGERPRINT}
    """
    tokens = parse.comma_separated_list(input)
    output: list[Link] = []
    for token in tokens:
        if ":" in token:
            subtokens = token.split(":", maxsplit=1)
            uid = subtokens[0]
            fingerprint = subtokens[1]
            output.append(Link(uid, fingerprint=fingerprint))
        else:
            output.append(Link(token, fingerprint=None))
    return output


# def parse_flag(input: str | None) -> bool:
#     if input:
#         raise ValueError("not expecting a value")
#     return True


def parse_str(input: str | None) -> str | None:
    if input:
        return input
    return None


@dataclass
class Args:
    """Parsed arguments for the Vertex directive."""

    uid: str
    parents: list[Link] = field(default_factory=list)
    layout: str = DEFAULT_FORMATTER


class Directive(SphinxDirective):
    """An RST node representing a To-Do item."""

    has_content = True
    required_arguments = 1
    option_spec = {
        "parents": parse_parents,
        "layout": parse_str,
    }

    def run(self) -> Sequence[nodes.Node]:
        """Run the directive and return a Vertex node."""
        args = Args(uid=self.arguments[0], **self.options)

        text = "\n".join(self.content)

        fingerprint = base64.b64encode(hashlib.md5(text.encode()).digest())[:4].decode()

        content_node = Node(text)
        self.state.nested_parse(self.content, self.content_offset, content_node)

        targetnode = nodes.target("", "", ids=[args.uid])
        placeholder_node = Node(ids=[args.uid])

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
