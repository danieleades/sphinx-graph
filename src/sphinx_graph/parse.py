"""Utility functions for parsing restructered text directives into options."""
from __future__ import annotations


def comma_separated_list(input: str | None) -> list[str]:
    """Parse a comma-separated list of strings."""
    if input is None:
        return []
    return [link.strip() for link in input.split(",")]
