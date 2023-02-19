"""Custom configuration for Sphinx Graph."""

from __future__ import annotations

from dataclasses import dataclass, field

from sphinx_graph import vertex


@dataclass
class Config:
    """Configuration for the sphinx-graph extension.

    Example::

        from sphinx_graph import Config, VertexConfig

        graph_config = Config(
            vertex_config = VertexConfig(
                # this is the default value
                require_fingerprints=False,
            ),
            types = {
                "req": VertexConfig(
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

    vertex_config: vertex.Config = field(default_factory=vertex.Config)
    types: dict[str, vertex.Config] = field(default_factory=dict)
