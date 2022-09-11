"""Sphinx Directive for Vertex objects."""

from dataclasses import dataclass, field
from typing import List, Sequence

from docutils import nodes
from sphinx.util.docutils import SphinxDirective

from sphinx_graph import parse
from sphinx_graph.directives.vertex.context import get_context
from sphinx_graph.directives.vertex.info import Info
from sphinx_graph.directives.vertex.node import Node

__all__ = [
    "Directive",
]


@dataclass
class Args:
    """Parsed arguments for the Vertex directive."""

    uid: str
    parents: List[str] = field(default_factory=list)


class Directive(SphinxDirective):
    """An RST node representing a To-Do item."""

    has_content = True
    required_arguments = 1
    option_spec = {
        "parents": parse.list,
    }

    def run(self) -> Sequence[nodes.Node]:
        """Run the directive and return a Vertex node."""
        args = Args(uid=self.arguments[0], **self.options)

        content_node = Node("\n".join(self.content))
        self.state.nested_parse(self.content, self.content_offset, content_node)

        targetnode = nodes.target("", "", ids=[args.uid])
        placeholder_node = Node(ids=[args.uid])

        with get_context(self.env) as context:
            context.insert_vertex(
                args.uid,
                Info(
                    docname=self.env.docname,
                    lineno=self.lineno,
                    node=content_node,
                    target=targetnode,
                    parents=args.parents,
                ),
            )

        return [targetnode, placeholder_node]


def format_node(id: str, info: Info) -> nodes.Node:
    """Generate a formatted vertex, ready for insertion into the document."""
    table: nodes.Node = nodes.table()
    tgroup = nodes.tgroup(cols=1)
    colspec = nodes.colspec(colwidth=1)
    tgroup.append(colspec)
    table += tgroup

    thead = nodes.thead()
    tgroup += thead
    row = nodes.row()
    entry = nodes.entry()
    entry += nodes.paragraph(text=f"Requirement: {id}")
    row += entry

    thead.append(row)

    tbody = nodes.tbody()

    # add content
    row = nodes.row()
    entry = nodes.entry()
    entry += info.node
    row += entry

    tbody.append(row)

    tgroup += tbody

    return table
