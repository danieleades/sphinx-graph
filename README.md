# Sphinx Graph

[![codecov](https://codecov.io/gh/danieleades/sphinx-graph/branch/main/graph/badge.svg?token=WLPNTQXHrK)](https://codecov.io/gh/danieleades/sphinx-graph)
[![CI](https://github.com/danieleades/sphinx-graph/actions/workflows/ci.yaml/badge.svg)](https://github.com/danieleades/sphinx-graph/actions/workflows/ci.yaml)
[![sponsor](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/danieleades)
[![Documentation Status](https://readthedocs.org/projects/sphinx-graph/badge/?version=main)](https://sphinx-graph.readthedocs.io/en/main/?badge=main)

'Sphinx-Graph' is a plain-text, VCS-friendly, requirements management tool.

With Sphinx-Graph you define relationships between items in a document. These items form a directed acyclic graph (DAG). The extension-

- checks for cyclic references
- populates items with links to their 'neighbours'
- (optionally) tracks a hash of each item to trigger reviews when any parents change

Sphinx Graph is *heavily* inspired by [Sphinx-Needs](https://github.com/useblocks/sphinx-needs). Sphinx-Graph started life as a proof of concept refactor of Sphinx-Needs using modern python and strict type checking.

- Sphinx-Needs is the full-featured, grand-daddy of Sphinx-Graph
- By comparison, Sphinx-Graph is streamlined, and focuses on a much smaller feature set

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

For more information, see [the docs](https://sphinx-graph.readthedocs.io/en/main/).

or, build the local docs-

      cd docs
      poetry run make html

---

*Was this useful? [Buy me a coffee](https://github.com/sponsors/danieleades/sponsorships?sponsor=danieleades&preview=true&frequency=recurring&amount=5)*
