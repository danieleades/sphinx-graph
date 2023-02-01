"""Custom configuration for Sphinx Graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from re import Pattern


@dataclass
class VertexConfig:
    """Optional additional configuration for a vertex directive.

    Args:
        require_fingerprints:
            Whether parent links *must* provide fingerprints.
            If ``False`` (the default) then link fingerprints are checked
            if set, and ignored otherwise.
        layout: which of the default layouts to use.
            The options are "subtle" or "transparent".
        regex: A regex pattern to check vertex IDs against.
    """

    require_fingerprints: bool | None = None
    layout: str | None = None
    regex: Pattern[str] | None = None

    def override(self, other: VertexConfig) -> VertexConfig:
        """Override a VertexConfig by overlaying a second config."""
        return VertexConfig(
            require_fingerprints=(
                self.require_fingerprints
                if other.require_fingerprints is None
                else other.require_fingerprints
            ),
            layout=self.layout if other.layout is None else other.layout,
            regex=self.regex if other.regex is None else other.regex,
        )


@dataclass
class Config:
    """Configuration for the sphinx-graph extension.

    Example::

        from sphinx_graph import Config, DirectiveConfig

        graph_config = Config(
            vertex_config = DirectiveConfig(
                # this is the default value
                require_fingerprints=False,
            ),
            types = {
                "req": DirectiveConfig(
                    # any directives with the 'req' type will require fingerprints
                    require_fingerprints=True,
                    # IDs must be of the form "REQ-0000", etc.
                    regex=re.compile(r"^REQ-[0-9]{4}$"),
                )
            },
        )

    Args:
        vertex_config: Default configuration to apply to all vertices.
            The default configuration is overridden by any config set for a
            specific 'type' of vertex. That is in turn overridden by any configuration
            set directly on the vertex directive.
        types: Set default directive configuration for 'types' of vertices.
    """

    vertex_config: VertexConfig = field(default_factory=VertexConfig)
    types: dict[str, VertexConfig] = field(default_factory=dict)
