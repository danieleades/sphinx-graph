"""Docutils Vertex node.

This node is used as a placeholder only, and is replaced after parsing the entire graph.
"""

from __future__ import annotations

from docutils import nodes


class VertexNode(nodes.General, nodes.Element):
    """An RST node representing a Vertex."""
