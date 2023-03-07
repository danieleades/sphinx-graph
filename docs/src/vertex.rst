The Vertex Node
---------------

The core feature of Sphinx-Graph is the vertex directive. The vertex directive is used to wrap an
arbitrary document element and augment it with additional information. Each vertex directive forms
a node in a graph of related nodes.

This is particularly useful for tracking relationships between requirements, specifications, or any
other item used for plain-text requirements management.

.. code-block:: rst

    .. vertex:: node-001
        :tags: P1

        A vertex node can contain arbitrary content.

        .. note::

            That includes nested restructuredtext directives.

    .. vertex:: node-002
        :parents: node-001
        :tags: P2, ux

        Vertex nodes can have parent-child relationships to other nodes

this is rendered in place and augmented with additional information, like so:

.. vertex:: node-001
    :tags: P1

    A vertex node can contain arbitrary content

    .. note::

        That includes nested restructuredtext directives.

.. vertex:: node-002
    :parents: node-001
    :tags: P2, ux

    Vertex nodes can have parent-child relationships to other nodes


Fingerprints
============

Vertex nodes may optionally use 'fingerprints' to detect when a relationship between two nodes
must be reviewed (this is known as a 'suspect link').

A 'fingerprint' is a simple hash of the parent node's content. If the hash on the child node
doesn't match the content of the parent node, Sphinx-Graph will raise an error and inform the
user of the new hash.

Updating the hash silences the error, and signifies that the relationship between the nodes has
been reviewed and accepted.

The *first* time you add a fingerprint you can add an arbitrary value. At build time, the correct value will be calculcated and reported as a build error.

.. code-block:: rst

    .. vertex:: node-003

        A user story

    .. vertex:: node-004
        :parents: node-003:1234

        in this case '1234' is the (example) fingerprint of the relationship.
        if '1234' is the wrong hash (it is), then Sphinx-Graph will raise an error so that it can
        be updated to the correct value.

output:

.. epigraph::
    WARNING: suspect link found. vertex node-004 is linked to vertex node-003 with a fingerprint of '1234', but node-003's fingerprint is 'c6Rq'.
    node-004 should be reviewed, and the link fingerprint manually updated.

Configuration
=============

For information on global configuration, see :py:class:`sphinx_graph.config.Config`.

For information on vertex configuration, see :py:class:`sphinx_graph.vertex.config.Config`.

There are three locations that a vertex node can be configured.

1. global configuration in *conf.py*
2. *per-type* configuration in *confy.py*
3. local configuration directly on the vertex directive

Global configuration is overwritten by *per-type* configuration, which is in turn overwritten by
local configuration.

Global Vertex Configuration
...........................

*conf.py*

.. code-block:: python

    # ...

    graph_config = Config(
        vertex_config=VertexConfig(
            require_fingerprints=True,
            regex=re.compile(r"^REQ-[0-9]{4}$")
        )
    )

Per-Type Vertex Configuration
.............................

*conf.py*

.. code-block:: python

    # ...

    graph_config = Config(
        types={
            "mrd": VertexConfig(layout="transparent", regex=re.compile(r"^MRD-[0-9]{3}$")),
            "usr": VertexConfig(regex=re.compile(r"^USR-[0-9]{3}$")),
            "sys": VertexConfig(regex=re.compile(r"^SYS-[0-9]{3}$")),
        },
    )

*your-docs.rst*

.. code-block:: rst

    .. vertex:: USR-001
        :type: usr

        the ID will be checked and the layout chosen according the 'type' of vertex which has been configured.

Local Vertex Configuration
..........................

.. code-block:: rst

    .. vertex:: node-004
        :parents: node-003:1234
        :require_fingerprints:
        :layout: transparent

        (content)
