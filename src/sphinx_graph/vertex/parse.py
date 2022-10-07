"""Utility functions for parsing restructered text directives into options."""
from __future__ import annotations

from sphinx_graph.vertex.info import Link


def comma_separated_list(list_str: str | None) -> list[str]:
    """Parse a comma-separated list of strings."""
    if list_str is None:
        return []
    return [link.strip() for link in list_str.split(",")]


def parents(input: str | None) -> list[Link]:
    """Parse a comma separated list of parent link specifications.

    each element in the list may be in one of two forms

    - {PARENT_ID}
    - {PARENT_ID}:{PARENT_FINGERPRINT}
    """
    tokens = comma_separated_list(input)
    output: list[Link] = []
    for token in tokens:
        if ":" in token:
            subtokens = token.split(":", maxsplit=1)
            uid = subtokens[0]
            fingerprint = subtokens[1]
            output.append(Link(uid, fingerprint=fingerprint))
        else:
            output.append(Link(token, fingerprint=None))
    return output


def string(input: str | None) -> str | None:
    if input:
        return input
    return None
