"""Vertex-specific configuration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from re import Pattern


@dataclass
class Config:
    """Optional additional configuration for a vertex directive.

    Args:
        require_fingerprints:
            Whether parent links *must* provide fingerprints.
            If ``False`` (the default) then link fingerprints are checked
            if set, and ignored otherwise.
        layout: which of the built-in layouts to use.
            The options are "subtle" (the default) or "transparent".
        regex: A regex pattern to check vertex IDs against.
    """

    require_fingerprints: bool | None = None
    layout: str | None = None
    regex: Pattern[str] | None = None

    def override(self, other: Config) -> Config:
        """Override a Config by overlaying a second config."""
        return Config(
            require_fingerprints=(
                self.require_fingerprints
                if other.require_fingerprints is None
                else other.require_fingerprints
            ),
            layout=self.layout if other.layout is None else other.layout,
            regex=self.regex if other.regex is None else other.regex,
        )
