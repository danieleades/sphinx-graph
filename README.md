# Sphinx Graph

test PR

[![codecov](https://codecov.io/gh/danieleades/sphinx-graph/branch/main/graph/badge.svg?token=WLPNTQXHrK)](https://codecov.io/gh/danieleades/sphinx-graph)
[![CI](https://github.com/danieleades/sphinx-graph/actions/workflows/ci.yaml/badge.svg)](https://github.com/danieleades/sphinx-graph/actions/workflows/ci.yaml)
[![sponsor](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/danieleades)
[![Documentation Status](https://readthedocs.org/projects/sphinx-graph/badge/?version=main)](https://sphinx-graph.readthedocs.io/en/main/?badge=main)

'Sphinx-Graph' is a sphinx extension for plain-text, VCS-friendly, requirements management.

## Key Features

1. **Vertex Directive**: Define relationships between document elements.
2. **Vertex Table**: Generate summary tables of vertices.
3. **Fingerprinting**: Track changes and trigger reviews when parent elements are modified.
4. **Customizable Layouts**: Choose how vertices are displayed in your documentation.

With Sphinx-Graph you define relationships between items in a document. These items form a directed acyclic graph (DAG). The extension:

- Checks for cyclic references
- Populates items with links to their 'parents' or 'children'
- (Optionally) tracks a hash of each item to trigger reviews when any parents change

## Getting Started

Install Sphinx-Graph using pip:

```bash
pip install sphinx-graph
```

Add it to your Sphinx project's `conf.py`:

```python
extensions = [
   # ... other extensions ...
   "sphinx_graph",
]
```

## Vertices

The core sphinx directive provided by this extension is a 'Vertex'. A Vertex directive can be used to define relationships between text elements.

```rst
.. vertex:: USR-001

   this is a user requirement.

   This user requirement forms the basis of derived system requirements. When it is rendered in a
   sphinx document it will be augmented with links to any child vertices.

.. vertex:: SYS-001
   :parents: USR-001

   this is system requirement of some sort.

   It is derived from a higher-level user requirement (USR-001).
   When it is rendered in a sphinx document, it will be augmented with links to its parent as well
   as any 'children'.

.. vertex:: SYS-002
   :parents: USR-001:iG91

   this is another system requirement. This time the link to USR-001 is tracking the 'fingerprint'
   of its parent.

   The fingerprint is a 4-character hash. If USR-001 is modified, then SYS-002 will fail the build
   until the fingerprint is updated (the build error provides the new fingerprint). This means that
   changing a Vertex will trigger a review of all dependent vertices.
```

## Generating Summary Tables

The `vertex-table` directive generates summary tables of vertices:

```rst
.. vertex-table::
   :query: descendants

   uid = "REQ-001"
```

This will create a table showing REQ-001 and all its descendants.

## Benefits of Sphinx-Graph

1. **Version Control Friendly**: Plain-text format works well with Git and other VCS.
2. **Flexible**: Define custom relationships between any elements in your documentation.
3. **Traceable**: Easily track dependencies and impact of changes.
4. **Integrated**: Seamlessly works within your Sphinx documentation.

## Comparison with Similar Projects

Sphinx Graph is *heavily* inspired by [Sphinx-Needs](https://github.com/useblocks/sphinx-needs). Sphinx-Graph started life as a proof-of-concept refactor of Sphinx-Needs using modern python and strict type checking.

**[Sphinx-Needs](https://github.com/useblocks/sphinx-needs):**

- Sphinx-Needs is a more complex, feature-rich solution for requirements management, but may be heavy-weight for some use-cases.
- Sphinx-Graph is smaller, more streamlined, and uses modern Python with strict type checking.
- Sphinx-Graph can track 'suspect links' and force reviews when linked requirements are modified.

**[Doorstop](https://github.com/doorstop-dev/doorstop):**

- Doorstop is a command-line tool and Python API for managing requirements as text files.
- Like Sphinx-Graph, Doorstop is lightweight and version-control friendly.
- Sphinx-Graph integrates directly with Sphinx documentation, while Doorstop requires additional setup for documentation integration.
- Sphinx-Graph offers more flexible relationship types between items compared to Doorstop's hierarchical structure.

**Traditional Requirements Management Tools (Doors, Enterprise Architect, etc):**

- Sphinx-Graph doesn't require complex workflows or specific expertise to maintain.
- It's more cost-effective (it's free).
- Can be maintained in plain-text alongside the code.


For more information, see [the docs](https://sphinx-graph.readthedocs.io/en/main/).

or, build the local docs-

```bash
cd docs
uv run make html
```

---

*Was this useful? [Buy me a coffee](https://github.com/sponsors/danieleades/sponsorships?sponsor=danieleades&preview=true&frequency=recurring&amount=5)*
