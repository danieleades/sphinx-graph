"""Utility methods for SphinxGraph."""

from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def unwrap(x: T | None) -> T:
    """Unwrap an optional value.

    Args:
        x: The optional value to unwrap.

    Returns:
        The unwrapped value.

    Raises:
        ValueError: If the value is None.
    """
    if x is None:
        raise ValueError("attempted to 'unwrap' a None value!")
    return x
