"""Sphinx Directive for Vertex objects."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, ClassVar

import toml
from sphinx.errors import SphinxError
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

from sphinx_graph import parse
from sphinx_graph.table.info import Info
from sphinx_graph.table.node import TableNode
from sphinx_graph.table.state import State

if TYPE_CHECKING:
    from collections.abc import Sequence

    from docutils import nodes
    from sphinx.util.typing import OptionSpec

logger = logging.getLogger(__name__)

__all__ = [
    "Directive",
]


class Directive(SphinxDirective):
    """An RST node representing a table of Vertices."""

    has_content = True
    required_arguments = 0
    option_spec: ClassVar[OptionSpec] = {
        "query": parse.string,
    }

    def run(self) -> Sequence[nodes.Node]:
        """Run the directive and return a Vertex node."""
        uid = uuid.uuid4()
        node = TableNode(graph_uid=uid)

        content = "\n".join(self.content)
        try:
            args = toml.loads(content)
        except toml.TomlDecodeError as exc:
            msg = f"invalid TOML in 'vertex-table' directive: {exc}"
            logger.error(
                msg,
                location=(self.env.docname, self.lineno),
            )
            raise SphinxError(msg) from exc

        with State.get(self.env) as state:
            state.insert(
                uid,
                Info(
                    docname=self.env.docname,
                    query=self.options.get("query"),
                    args=args,
                ),
            )

        return [node]
