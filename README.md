# Sphinx Graph

A proof-of-concept modern, strongly-typed implementation of the 'Sphinx-Needs' extension (Very early prototype).

a typed API provides

- static analysis/error checking
- IDE code completion
- self-documenting APIs

## Typed Configuration

custom configuration object is fully typed, providing a self-documenting configuration API.

*conf.py*
```python
from sphinx_graph import Config

graph_config = Config(include_vertices=True)
```
