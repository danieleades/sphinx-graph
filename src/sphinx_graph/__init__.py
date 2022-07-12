"""Entrypoint for the sphinx-todo extension."""

from typing import Iterable, List, TypedDict

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.environment import BuildEnvironment
from sphinx.locale import _

from sphinx_graph.config import Config
from sphinx_graph.context import get_context
from sphinx_graph.util import unwrap
from sphinx_graph.vertex.directive import VertexDirective
from sphinx_graph.vertex.info import VertexInfo
from sphinx_graph.vertex.node import Vertex

__all__ = [
    "Config",
]


class VertexList(nodes.General, nodes.Element):  # type: ignore[misc]
    """An RST node representing a list of Vertex items."""


def visit_vertex_node(self: nodes.GenericNodeVisitor, node: VertexList) -> None:
    self.visit_admonition(node)


def depart_vertex_node(self: nodes.GenericNodeVisitor, node: Vertex) -> None:
    self.depart_admonition(node)


class VertexlistDirective(Directive):
    """An RST directive which produces a To-Do list node."""

    def run(self) -> List[VertexList]:
        """Run the directive and return a ToDoList node."""
        return [VertexList("")]


def purge_vertices(_app: Sphinx, env: BuildEnvironment, docname: str) -> None:
    """
    Clear out all vertices whose docname matches the given one from the graph_all_vertices list.

    If there are vertices left in the document, they will be added again during parsing.
    """
    with get_context(env) as context:
        context.all_vertices = {
            id: vertex
            for id, vertex in context.all_vertices.items()
            if vertex.docname != docname
        }


def merge_vertices(
    _app: Sphinx, env: BuildEnvironment, _docnames: List[str], other: BuildEnvironment
) -> None:
    """Merge the vertices from multiple environments during parallel builds."""
    with get_context(env) as context, get_context(other) as other_context:
        context.all_vertices.update(other_context.all_vertices)


def build_vertex_list(
    builder: Builder,
    env: BuildEnvironment,
    fromdocname: str,
    all_vertices: Iterable[VertexInfo],
) -> Iterable[nodes.Node]:
    """Build a VertexList node."""
    for vertex_info in all_vertices:
        para = nodes.paragraph()
        filename = env.doc2path(vertex_info.docname, base=False)
        description = _(
            f"(The original entry is located in {filename},"
            f" line {vertex_info.lineno} and can be found "
        )
        para += nodes.Text(description)

        # Create a reference
        newnode = nodes.reference("", "")
        innernode = nodes.emphasis(_("here"), _("here"))
        newnode["refdocname"] = vertex_info.docname
        uri_base = builder.get_relative_uri(fromdocname, vertex_info.docname)
        newnode["refuri"] = f"{uri_base}#{vertex_info.target['refid']}"
        newnode.append(innernode)
        para += newnode
        para += nodes.Text(".)")

        # Insert into the VertexList
        yield vertex_info.node
        yield para


def process_vertex_nodes(
    app: Sphinx, doctree: nodes.document, fromdocname: str
) -> None:
    """Process Vertex nodes into VertexList nodes."""
    config: Config = app.config.graph_config
    if not config.include_vertices:
        for vertex_node in doctree.findall(Vertex):
            vertex_node.parent.remove(vertex_node)  # type: ignore[union-attr]

    # Replace all VertexList nodes with a list of the collected vertices.
    # Augment each vertex with a backlink to the original location.
    builder = unwrap(app.builder)
    env = unwrap(builder.env)

    # get the list of todos from the environment
    with get_context(env) as context:

        for vertexlist_node in doctree.findall(VertexList):
            if not config.include_vertices:
                vertexlist_node.replace_self([])
                continue

            content = list(
                build_vertex_list(
                    builder, env, fromdocname, context.all_vertices.values()
                )
            )
            vertexlist_node.replace_self(content)


def generate_graph(app: Sphinx, _doctree: nodes.document, _fromdocname: str) -> None:
    """Generate a graph of all vertices in the document."""
    builder = unwrap(app.builder)
    env = unwrap(builder.env)

    # get the list of vertices from the environment and compose them into a directed graph
    with get_context(env) as context:
        graph = context.graph
        for uid, vertex_info in context.all_vertices.items():
            # add each node
            graph.add_node(uid)

            # add all 'child' edges
            for child in vertex_info.children:
                graph.add_edge(child, uid)

            # add all 'parent' edges
            for parent in vertex_info.parents:
                graph.add_edge(uid, parent)


class ExtensionMetadata(TypedDict):
    """The metadata returned by this extension."""

    version: str
    env_version: int
    parallel_read_safe: bool
    parallel_write_safe: bool


def setup(app: Sphinx) -> ExtensionMetadata:
    """Set up the sphinx-graph extension."""
    app.add_config_value("graph_config", Config(), "", types=(Config))

    app.add_node(VertexList)
    app.add_node(
        Vertex,
        html=(visit_vertex_node, depart_vertex_node),
        latex=(visit_vertex_node, depart_vertex_node),
        text=(visit_vertex_node, depart_vertex_node),
    )

    app.add_directive("vertexlist", VertexlistDirective)
    app.add_directive("vertex", VertexDirective)
    app.connect("doctree-resolved", process_vertex_nodes)
    app.connect("doctree-resolved", generate_graph)
    app.connect("env-purge-doc", purge_vertices)
    app.connect("env-merge-info", merge_vertices)

    return {
        "version": "0.1",
        "env_version": 0,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
