from docutils import nodes


class Node(nodes.General, nodes.Element):  # type: ignore[misc]
    """An RST node representing a Vertex."""
