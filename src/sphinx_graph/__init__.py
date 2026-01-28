"""Sphinx-Graph public API.

add the sphinx-graph extension to your sphinx project by
adding it to ``conf.py``:

.. code:: python

    extensions = [
        "sphinx_graph",
    ]
"""

from . import vertex
from ._setup import setup
from .config import Config
from .vertex import Config as VertexConfig
from .vertex import Query

__all__ = [
    "Config",
    "Query",
    "VertexConfig",
    "setup",
    "vertex",
]
