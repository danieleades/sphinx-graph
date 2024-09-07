"""vertex-table directive information dataclass."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Info:
    """A dataclass which captures the information needed to construct a vertex-table.

    Args:
        docname: the name of the document where the table is located
        query: the name of a query used to filter and sort vertices for display
        args: keyword arguments to be passed to the query
    """

    docname: str
    query: str | None
    args: dict[str, Any]
