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

Sphinx-Graph supports using queries to sort and filter the vertices displayed in a vertex table.

Signature
.........

A query is a Python callable with the type :py:data:`sphinx_graph.vertex.Query`.
In practice, this means:

.. code-block:: python

    # first parameter must be a State; additional parameters are allowed
    from collections.abc import Iterable
    from sphinx_graph.vertex import State

    def my_query(state: State, *, kwarg1: str, kwarg2: int = 0) -> Iterable[str]:
        ...

- The first parameter is always :py:class:`sphinx_graph.vertex.state.State`, which contains the
  parsed vertices and a graph of their relationships.
- The function returns an iterable of vertex UIDs in the order they should be displayed.
- Additional parameters are supported. As the directive passes only keyword arguments, it is
  recommended to declare them as keyword-only (using `*`) and provide sensible defaults.

Configuration
.............

Queries are defined in the global configuration in ``conf.py`` and then referenced by name in
the ``vertex-table`` directive. See :py:class:`sphinx_graph.config.Config` for details.

Passing Arguments from the Directive
...................................

Keyword arguments are parsed from the directive body as TOML and passed to the query function
as keyword arguments.

.. code-block:: rst

    .. vertex-table::
       :query: my_query

       # TOML syntax is used to pass kwargs to the query
       kwarg1 = "value"
       kwarg2 = 1234

Notes
.....

- Only keyword arguments are supported via the directive body; positional arguments are not used.
- Extra keys in the TOML body that the query does not accept will raise a TypeError at runtime
  unless the query includes a catch-all (e.g., ``**_kwargs``).
