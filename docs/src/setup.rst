Setup
-----

Installation
============

Install using Pip

        pip install sphinx-graph

Or Poetry

        poetry add sphinx-graph

And add to the 'extensions' in your Sphinx document's *conf.py* file

.. code-block:: python

    # conf.py

    project = "your-documentation"

    extensions = [
        "sphinx_graph",
    ]

.. _global configuration:

Configuration
=============

See :py:class:`sphinx_graph.config.Config`.
