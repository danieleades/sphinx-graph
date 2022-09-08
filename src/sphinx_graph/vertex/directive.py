"""Sphinx Directive for Vertex objects."""

from dataclasses import dataclass, field
from typing import List, Optional, Sequence

from docutils import nodes
from sphinx.util.docutils import SphinxDirective

from sphinx_graph.context import get_context
from sphinx_graph.vertex.info import VertexInfo
from sphinx_graph.vertex.node import VertexNode
from sphinx.application import Sphinx
from sphinx_graph.util import unwrap

__all__ = [
    "VertexDirective",
]


def parse_list(input: Optional[str]) -> List[str]:
    """Parse a comma-separated list of strings."""
    if input is None:
        return []
    return [link.strip() for link in input.split(",")]


@dataclass
class Args:
    """Parsed arguments for the Vertex directive."""

    uid: str
    parents: List[str] = field(default_factory=list)
    children: List[str] = field(default_factory=list)


class VertexDirective(SphinxDirective):
    """An RST node representing a To-Do item."""

    has_content = True
    required_arguments = 1
    option_spec = {
        "parents": parse_list,
        "children": parse_list,
    }

    def run(self) -> Sequence[nodes.Node]:
        """Run the directive and return a Vertex node."""
        args = Args(uid=self.arguments[0], **self.options)

        content_node = VertexNode("\n".join(self.content))
        self.state.nested_parse(self.content, self.content_offset, content_node)

        targetnode = nodes.target("", "", ids=[args.uid])
        placeholder_node = VertexNode(ids=[args.uid])

        with get_context(self.env) as context:
            context.insert_vertex(
                args.uid,
                VertexInfo(
                    docname=self.env.docname,
                    lineno=self.lineno,
                    node=content_node,
                    target=targetnode,
                    parents=args.parents,
                ),
            )

        return [targetnode, placeholder_node]


def process(
    app: Sphinx, doctree: nodes.document, _fromdocname: str
) -> None:
    """Process Vertex nodes by formatting and adding links to graph neighbours."""

    builder = unwrap(app.builder)
    env = unwrap(builder.env)

    # get the list of todos from the environment
    with get_context(env) as context:

        print("test")

        for vertex_node in doctree.findall(VertexNode):
            id = vertex_node.attributes["ids"][0]
            info = context.all_vertices[id]

            print(info.node)

            vertex_node.replace_self(info.node)
