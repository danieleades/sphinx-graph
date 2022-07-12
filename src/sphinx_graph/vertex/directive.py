"""Sphinx Directive for Vertex objects."""

from dataclasses import dataclass, field
from typing import List, Optional, Sequence

from docutils import nodes
from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective

from sphinx_graph.context import get_context
from sphinx_graph.vertex.info import VertexInfo
from sphinx_graph.vertex.node import Vertex

__all__ = [
    "VertexDirective",
]


def parse_list(input: Optional[str]) -> List[str]:
    if input is None:
        return []
    return [link.strip() for link in input.split(",")]


@dataclass
class Args:
    id: str
    parents: List[str] = field(default_factory=list)
    siblings: List[str] = field(default_factory=list)
    children: List[str] = field(default_factory=list)


class VertexDirective(SphinxDirective):
    """An RST node representing a To-Do item."""

    has_content = True
    required_arguments = 1
    option_spec = {
        "parents": parse_list,
        "siblings": parse_list,
        "children": parse_list,
    }

    def run(self) -> Sequence[nodes.Node]:
        """Run the directive and return a Vertex node."""
        # _args = Args(id=self.arguments[0], **self.options)
        targetid = f"vertex-{self.env.new_serialno('graph')}"
        targetnode = nodes.target("", "", ids=[targetid])

        vertex_node = Vertex("\n".join(self.content))
        vertex_node += nodes.title(_("Vertex"), _("Vertex"))
        self.state.nested_parse(self.content, self.content_offset, vertex_node)

        with get_context(self.env) as context:
            context.all_vertices.append(
                VertexInfo(
                    docname=self.env.docname,
                    lineno=self.lineno,
                    vertex=vertex_node.deepcopy(),
                    target=targetnode,
                )
            )

        return [targetnode, vertex_node]
