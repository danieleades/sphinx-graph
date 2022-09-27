"""Lifecycle events specific to the Vertex node."""

from __future__ import annotations

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.util import logging

from sphinx_graph.config import Config
from sphinx_graph.directives.vertex.info import InfoParsed
from sphinx_graph.directives.vertex.layout import (
    DEFAULT_FORMATTER,
    FORMATTERS,
    apply_formatting,
)
from sphinx_graph.directives.vertex.node import Node
from sphinx_graph.directives.vertex.state import get_state
from sphinx_graph.util import unwrap

logger = logging.getLogger(__name__)


def visit_node(_self: nodes.GenericNodeVisitor, _node: Node) -> None:
    """
    Visits the Vertex node.

    This method is a no-op
    """


def depart_node(_self: nodes.GenericNodeVisitor, _node: Node) -> None:
    """
    Visits the Vertex node.

    This method is a no-op
    """


def process(app: Sphinx, doctree: nodes.document, _fromdocname: str) -> None:
    """Process Vertex nodes by formatting and adding links to graph neighbours."""
    builder = unwrap(app.builder)
    env = unwrap(builder.env)
    config: Config = app.config.graph_config
    formatters = {**FORMATTERS, **config.custom_layouts}

    # get the list of todos from the environment
    with get_state(env) as state:

        for vertex_node in doctree.findall(Node):
            print(vertex_node.attributes)
            uid = vertex_node["graph_uid"]
            info = state.all_vertices[uid]
            children = list(state.graph.predecessors(uid))
            info_parsed = InfoParsed.from_info(uid, info, children)
            layout = info.layout or "table"
            if layout not in formatters:
                logger.error(
                    f"vertex {uid} has unknown layout '{layout}'. Defaulting to '{DEFAULT_FORMATTER}' layout."
                )
                layout = DEFAULT_FORMATTER

            formatter = formatters[layout]
            vertex_node.replace_self(
                apply_formatting(formatter, state, builder, info_parsed)
            )


def purge(_app: Sphinx, env: BuildEnvironment, docname: str) -> None:
    """
    Clear out all vertices whose docname matches the given one from the graph_all_vertices list.

    If there are vertices left in the document, they will be added again during parsing.
    """
    with get_state(env) as state:
        state.all_vertices = {
            id: vert
            for id, vert in state.all_vertices.items()
            if vert.docname != docname
        }


def merge(
    _app: Sphinx, env: BuildEnvironment, _docnames: list[str], other: BuildEnvironment
) -> None:
    """Merge the vertices from multiple environments during parallel builds."""
    with get_state(env) as state, get_state(other) as other_state:
        state.all_vertices.update(other_state.all_vertices)
