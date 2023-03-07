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

A query is a python function with a signature of

.. code-block:: python

    Callable[[sphinx_graph.vertex.State], Iterable[str]]

where :py:class:`sphinx_graph.vertex.state.State` captures the list of available vertices and their associated info parsed from the
document tree, as well as a networkx.DiGraph of the relationships between vertex nodes. The return value is a list of the vertices to display,
in the order in which they should be displayed.

The query may also accept additional keyword arguments (with or without defaults).

Queries are defined in the global configuration in *conf.py* and then referenced in the 'vertex-table' directive.
See :py:class:`sphinx_graph.config.Config` for details.

Keyword arguments are parsed from the body of the directive in the TOML format.

.. code-block:: rst

    .. vertex-table::
        :my_query:

        # TOML syntax is used to pass in kwargs for the query
        kwarg1 = "value"
        kwarg2 = 1234
