"""Utility functions for parsing restructered text directives into options."""
from __future__ import annotations


def comma_separated_list(list_str: str | None) -> list[str]:
    """Parse a comma-separated list of strings."""
    if list_str is None:
        return []
    return [link.strip() for link in list_str.split(",")]
