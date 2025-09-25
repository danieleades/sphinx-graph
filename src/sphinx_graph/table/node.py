"""Docutils vertex-table node.

This node is a placeholder and is replaced after parsing the entire graph.
"""

from __future__ import annotations

from docutils import nodes


class TableNode(nodes.General, nodes.Element):
    """An RST node representing a table of vertices."""
