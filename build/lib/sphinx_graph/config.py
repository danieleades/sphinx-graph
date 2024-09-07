"""Custom configuration for Sphinx Graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from sphinx_graph import vertex

if TYPE_CHECKING:
    from sphinx_graph.vertex.query import Query


@dataclass
class Config:
    """Configuration for the sphinx-graph extension.

    Example::

        from sphinx_graph import Config, VertexConfig

        # custom vertex search/filter queries
        import queries

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
            queries = {
                "ancestors": query.ancestors,
            }
        )

    Args:
        vertex_config: Default configuration to apply to all vertices.
            This is an instance of :py:class:`sphinx_graph.vertex.config.Config`.
            The default configuration is overridden by any config set for a
            specific 'type' of vertex. That is in turn overridden by any configuration
            set directly on the vertex directive.
        types: Set default directive configuration for 'types' of vertices.
            This is mapping from type name to
            :py:class:`sphinx_graph.vertex.config.Config`
        queries: Functions used to filter and sort vertices for display in tables.
            A 'query' is a method which accepts a `sphinx_graph.vertex.State` and
            returns a list of vertex UIDs (typed as `sphinx_graph.Query`).

            It is used for filtering and sorting vertices for display in a
            'vertex table'.

            .. code:: python

                # my_queries.py

                from sphinx_graph.vertex import State

                def my_query(state: State) -> Iterable[str]:
                    # TODO: parse the 'State' object and return a list of vertex UIDs
                    # ...

            .. code:: python

                # conf.py

                from sphinx_graph import Config

                from my_queries import my_query


                graph_config = Config(
                    queries = {
                        "my_query": my_query,
                    }
                )

            .. warning::

                Due to a quirk in the way Sphinx handles *conf.py*, the query function
                MUST be defined in a different file and imported into *conf.py*.
    """

    vertex_config: vertex.Config = field(default_factory=vertex.Config)
    types: dict[str, vertex.Config] = field(default_factory=dict)
    queries: dict[str, Query] = field(default_factory=dict)
