"""Sphinx Directive for Vertex objects."""

from __future__ import annotations

import base64
import hashlib
from typing import Sequence

from docutils import nodes
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import nested_parse_with_titles
from sphinx.util.typing import OptionSpec

from sphinx_graph import parse
from sphinx_graph.config import Config, VertexConfig
from sphinx_graph.info import Info
from sphinx_graph.node import Node as VertexNode
from sphinx_graph.state import State

__all__ = [
    "Directive",
]


class Directive(SphinxDirective):
    """An RST node representing a To-Do item."""

    has_content = True
    required_arguments = 1
    option_spec: OptionSpec = {
        "parents": parse.parents,
        "layout": parse.string,
        "require_fingerprints": parse.boolean,
        "type": parse.string,
    }

    def run(self) -> Sequence[nodes.Node]:
        """Run the directive and return a Vertex node."""
        uid = self.arguments[0]
        content_node = VertexNode(graph_uid=uid)
        nested_parse_with_titles(self.state, self.content, content_node)

        fingerprint = base64.b64encode(
            hashlib.md5(content_node.astext().encode()).digest()
        )[:4].decode()

        with State.get(self.env) as state:
            state.insert_vertex(
                uid,
                Info(
                    docname=self.env.docname,
                    config=self._vertex_config(),
                    parents=self.options.get("parents", {}),
                    fingerprint=fingerprint,
                ),
            )

        targetnode = nodes.target("", "", ids=[uid])

        return [targetnode, content_node]

    def _default_config(self) -> VertexConfig:
        config: Config = self.env.app.config.graph_config
        return config.vertex_config

    def _directive_config(self) -> VertexConfig:
        return VertexConfig(
            require_fingerprints=self.options.get("require_fingerprints"),
            layout=self.options.get("layout"),
        )

    def _type_config(self) -> VertexConfig:
        config: Config = self.env.app.config.graph_config
        vertex_type = self.options.get("type")
        if vertex_type:
            return config.types[vertex_type]
        else:
            return VertexConfig()

    def _vertex_config(self) -> VertexConfig:
        return (
            self._default_config()
            ._override(self._type_config())
            ._override(self._directive_config())
        )
