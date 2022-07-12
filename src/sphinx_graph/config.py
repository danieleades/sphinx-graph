"""Custom configuration for Sphinx Graph."""

from dataclasses import dataclass


@dataclass
class Config:
    """Configuration object for Sphinx Graph.

    Args:
        include_vertices: Whether to include vertices in the output.
    """

    include_vertices: bool = False
