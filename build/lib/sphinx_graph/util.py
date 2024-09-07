"""Utility methods for SphinxGraph."""

from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def unwrap(option: T | None) -> T:
    """Unwrap an optional value.

    Args:
        option: The optional value to unwrap.

    Returns:
        The unwrapped value.

    Raises:
        ValueError: If the value is None.
    """
    if option is None:
        err_msg = "attempted to 'unwrap' a None value!"
        raise ValueError(err_msg)
    return option
