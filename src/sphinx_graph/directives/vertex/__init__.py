"""Sphinx Directive for Vertex objects."""

from dataclasses import dataclass, field
from typing import List, Optional, Sequence

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.environment import BuildEnvironment

from sphinx_graph.directives.vertex.context import get_context
from sphinx_graph.util import unwrap
from sphinx_graph.directives.vertex.info import Info
from sphinx_graph.directives.vertex.node import Node

__all__ = [
    "Directive",
    "Info",
    "Node",
    "visit_node",
    "depart_node",
    "process",
    "purge",
    "merge",
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


class Directive(SphinxDirective):
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


def format(id: str, info: Info) -> nodes.Node:
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


# Event handlers

def visit_node(_self: nodes.GenericNodeVisitor, _node: Node) -> None:
    pass


def depart_node(_self: nodes.GenericNodeVisitor, _node: Node) -> None:
    pass


def process(app: Sphinx, doctree: nodes.document, _fromdocname: str) -> None:
    """Process Vertex nodes by formatting and adding links to graph neighbours."""
    builder = unwrap(app.builder)
    env = unwrap(builder.env)

    # get the list of todos from the environment
    with get_context(env) as context:

        for vertex_node in doctree.findall(Node):
            id = vertex_node.attributes["ids"][0]
            info = context.all_vertices[id]

            vertex_node.replace_self(format(id, info))


def purge(_app: Sphinx, env: BuildEnvironment, docname: str) -> None:
    """
    Clear out all vertices whose docname matches the given one from the graph_all_vertices list.

    If there are vertices left in the document, they will be added again during parsing.
    """
    with get_context(env) as context:
        context.all_vertices = {
            id: vert
            for id, vert in context.all_vertices.items()
            if vert.docname != docname
        }


def merge(
    _app: Sphinx, env: BuildEnvironment, _docnames: List[str], other: BuildEnvironment
) -> None:
    """Merge the vertices from multiple environments during parallel builds."""
    with get_context(env) as context, get_context(other) as other_context:
        context.all_vertices.update(other_context.all_vertices)
