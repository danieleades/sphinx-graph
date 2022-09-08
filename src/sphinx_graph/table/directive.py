"""Sphinx Directive for Vertex objects."""

from dataclasses import dataclass
from typing import Sequence

from docutils import nodes
from sphinx.util.docutils import SphinxDirective


__all__ = [
    "TableDirective",
]


@dataclass
class Args:
    """Parsed arguments for the Vertex directive."""


class TableDirective(SphinxDirective):
    """An RST node representing a To-Do item."""

    has_content = True
    required_arguments = 0

    def run(self) -> Sequence[nodes.Node]:
        """Run the directive and return a Vertex node."""
        table = nodes.table()

        # with get_context(self.env) as context:

        return [table]
