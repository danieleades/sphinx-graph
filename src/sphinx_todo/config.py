"""Custom configuration for Sphinx Graph."""

from dataclasses import dataclass


@dataclass
class Config:
    """Configuration object for Sphinx Graph.

    Args:
        include_todos: Whether to include todos in the output.
    """

    include_todos: bool = False
