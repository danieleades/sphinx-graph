"""Utility functions for parsing restructured text directives into options."""

from __future__ import annotations

from sphinx.errors import ConfigError


def boolean(value: str | None) -> bool:
    """Parse a boolean flag.

    Passing the flag without arguments is the same as using the value 'True'
    """
    if value is None:
        return True
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    err_msg = f"invalid boolean value: {value}"
    raise ConfigError(err_msg)


def comma_separated_list(list_str: str | None) -> list[str]:
    """Parse a comma-separated list of strings."""
    if list_str is None:
        return []
    return [link.strip() for link in list_str.split(",")]


def parents(value: str | None) -> dict[str, str | None]:
    """Parse a comma separated list of parent link specifications.

    each element in the list may be in one of two forms

    - {PARENT_ID}
    - {PARENT_ID}:{PARENT_FINGERPRINT}
    """
    tokens = comma_separated_list(value)
    output: dict[str, str | None] = {}
    for token in tokens:
        if ":" in token:
            subtokens = token.split(":", maxsplit=1)
            uid = subtokens[0]
            fingerprint = subtokens[1]
        else:
            uid = token
            fingerprint = None
        output[uid] = fingerprint
    return output


def string(value: str | None) -> str | None:
    """Parse a str input.

    Returns None if the input is None or an empty string
    """
    return value or None
