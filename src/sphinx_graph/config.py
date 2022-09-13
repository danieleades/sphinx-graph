"""Custom configuration for Sphinx Graph."""

from dataclasses import dataclass


@dataclass
class Config:
    """Configuration object for Sphinx Graph.

    Args:
        parents_require_fingerprints: Whether parent links require fingerprints
    """

    parents_require_fingerprints: bool = False
