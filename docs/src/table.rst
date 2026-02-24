Vertex Table
------------

a vertex table is a directive used to generate a summary of vertices in the vertex graph.

for example, this:

.. code-block:: rst

    .. vertex-table::

would produce the following table of vertices contained in this document
(see the example :doc:`/src/example/index`):

    .. vertex-table::

Queries
=======

Sphinx-Graph supports using 'queries' to sort and filter the vertices displayed in a vertex table.

A query is a Python function with the signature:

.. code-block:: python

    Callable[[sphinx_graph.vertex.State], Iterable[str]]

:py:class:`sphinx_graph.vertex.State` provides access to all vertices and the graph of relationships between them.
The return value is the list of vertex UIDs to display, in order.

Queries may also accept additional keyword arguments (with or without defaults), which are passed in from the directive body using TOML syntax.

Writing a query
---------------

Define the query function in a separate module (not directly in *conf.py*), then register it under a name in *conf.py*:

.. code-block:: python

    # my_queries.py

    from collections.abc import Iterable
    from sphinx_graph.vertex import State

    def by_tag(state: State, *, tag: str) -> Iterable[str]:
        """Return all vertices that have a given tag."""
        return (
            uid for uid, info in state.vertices.items()
            if tag in info.tags
        )

.. code-block:: python

    # conf.py

    from sphinx_graph import Config
    from my_queries import by_tag

    graph_config = Config(
        queries={"by_tag": by_tag},
    )

Then reference the query by name in a ``vertex-table`` directive:

.. code-block:: rst

    .. vertex-table::
        :by_tag:

        tag = "my-tag"

Keyword arguments are parsed from the directive body as TOML.
