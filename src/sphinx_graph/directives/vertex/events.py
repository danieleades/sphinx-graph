from typing import List

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment

from sphinx_graph.directives.vertex.context import get_context
from sphinx_graph.directives.vertex.directive import format_node
from sphinx_graph.util import unwrap
from sphinx_graph.directives.vertex.node import Node


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

            vertex_node.replace_self(format_node(id, info))


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
