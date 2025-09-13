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
            A query is a :py:data:`sphinx_graph.vertex.Query` — a callable whose
            first parameter is :py:class:`sphinx_graph.vertex.state.State` and
            which returns an iterable of vertex UIDs (``Iterable[str]``).

            Queries may declare additional parameters (typically keyword-only).
            When used by the ``vertex-table`` directive, keyword arguments are
            taken from the directive body (parsed as TOML) and passed through to
            the query function. Prefer keyword-only parameters (``*``) and
            provide defaults where appropriate.

            It is used for filtering and sorting vertices for display in a
            'vertex table'.

            .. code:: python

                # my_queries.py

                from sphinx_graph.vertex import State

                def my_query(state: State, *, uid: str, limit: int = 10) -> Iterable[str]:
                    # parse the 'State' object and return a list of vertex UIDs
                    # using values provided by the directive body
                    # ...

            .. code:: python

                # conf.py

                from sphinx_graph import Config

                from my_queries import my_query


                graph_config = Config(
                    queries={
                        "my_query": my_query,
                    }
                )

            In a document, reference the query and pass arguments via TOML:

            .. code:: rst

                .. vertex-table::
                   :query: my_query

                   uid = "REQ-001"
                   limit = 20

            .. warning::

                Due to a quirk in the way Sphinx handles *conf.py*, the query function
                MUST be defined in a different file and imported into *conf.py*.
    """

    vertex_config: vertex.Config = field(default_factory=vertex.Config)
    types: dict[str, vertex.Config] = field(default_factory=dict)
    queries: dict[str, Query] = field(default_factory=dict)
