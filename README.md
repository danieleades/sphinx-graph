# Sphinx Graph

[![codecov](https://codecov.io/gh/danieleades/sphinx-graph/branch/main/graph/badge.svg?token=WLPNTQXHrK)](https://codecov.io/gh/danieleades/sphinx-graph)
[![CI](https://github.com/danieleades/sphinx-graph/actions/workflows/ci.yaml/badge.svg)](https://github.com/danieleades/sphinx-graph/actions/workflows/ci.yaml)
[![sponsor](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/danieleades)

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
