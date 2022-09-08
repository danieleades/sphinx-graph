"""An RST node representing a Vertex."""

from docutils import nodes


class VertexNode(nodes.Admonition, nodes.Element):  # type: ignore[misc]
    """An RST node representing a Vertex."""
