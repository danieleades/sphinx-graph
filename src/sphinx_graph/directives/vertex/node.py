"""
Docutils Vertex node.

This node is used as a placeholder only, and is replaced after parsing the entire graph.
"""

from docutils import nodes


class Node(nodes.General, nodes.Element):  # type: ignore[misc]
    """An RST node representing a Vertex."""
