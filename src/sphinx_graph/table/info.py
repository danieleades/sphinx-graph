from dataclasses import dataclass
from typing import Any


@dataclass
class Info:
    docname: str
    query: str | None
    args: dict[str, Any]
