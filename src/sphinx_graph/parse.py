"""Utility functions for parsing restructered text directives into options."""
from __future__ import annotations

from sphinx.errors import ConfigError


def boolean(input: str | None) -> bool:
    """Parse a boolean flag.

    Passing the flag without arguments is the same as using the value 'True'
    """
    if input is None:
        return True
    if input.lower() == "true":
        return True
    if input.lower() == "false":
        return False

    raise ConfigError(f"invalid boolean value: {input}")


def comma_separated_list(list_str: str | None) -> list[str]:
    """Parse a comma-separated list of strings."""
    if list_str is None:
        return []
    return [link.strip() for link in list_str.split(",")]


def parents(input: str | None) -> dict[str, str | None]:
    """Parse a comma separated list of parent link specifications.

    each element in the list may be in one of two forms

    - {PARENT_ID}
    - {PARENT_ID}:{PARENT_FINGERPRINT}
    """
    tokens = comma_separated_list(input)
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


def string(input: str | None) -> str | None:
    """Parse a str input.

    Returns None if the input is None or an empty string
    """
    return input or None
