"""Dataclass objects will store information about a Vertex directive."""
from __future__ import annotations

from dataclasses import dataclass

from docutils import nodes


@dataclass
class Info:
    """Vertex information dataclass."""

    docname: str
    content: nodes.Element
