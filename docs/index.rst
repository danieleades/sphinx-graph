Welcome to sphinx-graph's documentation!
========================================

Sphinx-Graph is a powerful sphinx extension for plain-text requirements management. It provides a flexible and version-control friendly way to define, track, and visualize relationships between elements in your documentation.

Key Features
------------

1. **Vertex Directive**: Define relationships between document elements.
2. **Vertex Table**: Generate summary tables of vertices.
3. **Fingerprinting**: Track changes and trigger reviews when parent elements are modified.
4. **Customizable Layouts**: Choose how vertices are displayed in your documentation.

Getting Started
---------------

Install Sphinx-Graph using pip:

.. code-block:: bash

   pip install sphinx-graph

Add it to your Sphinx project's `conf.py`:

.. code-block:: python

   extensions = [
       # ... other extensions ...
       "sphinx_graph",
   ]

Using the Vertex Directive
--------------------------

The :doc:`vertex </src/vertex>` directive is the core feature of Sphinx-Graph. It allows you to define relationships between elements in your documentation:

.. code-block:: rst

   .. vertex:: REQ-001
      :tags: functional, high-priority

      The system shall provide user authentication.

   .. vertex:: REQ-002
      :parents: REQ-001
      :tags: functional

      The system shall support password-based authentication.

This creates a parent-child relationship between REQ-001 and REQ-002.

Generating Summary Tables
-------------------------

The :doc:`vertex-table </src/table>` directive generates summary tables of vertices:

.. code-block:: rst

   .. vertex-table::
      :query: descendants

      uid = "REQ-001"

This will create a table showing REQ-001 and all its descendants.

Benefits of Sphinx-Graph
------------------------

1. **Version Control Friendly**: Plain-text format works well with Git and other VCS.
2. **Flexible**: Define custom relationships between any elements in your documentation.
3. **Traceable**: Easily track dependencies and impact of changes.
4. **Integrated**: Seamlessly works within your Sphinx documentation.

Comparison with Similar Projects
--------------------------------

`Sphinx-Needs <https://github.com/useblocks/sphinx-needs>`_:

- Sphinx-Needs is a more complex, feature-rich solution for requirements management, but may be heavy-weight for some use-cases.
- Sphinx-Graph is smaller, more streamlined, and uses modern Python with strict type checking.
- Sphinx-Graph can track 'suspect links' and force reviews when linked requirements are modified.

`Doorstop <https://github.com/mtshulker/doorstop>`_:

- Doorstop is a command-line tool and Python API for managing requirements as text files.
- Like Sphinx-Graph, Doorstop is lightweight and version-control friendly.
- Sphinx-Graph integrates directly with Sphinx documentation, while Doorstop requires additional setup for documentation integration.
- Sphinx-Graph offers more flexible relationship types between items compared to Doorstop's hierarchical structure.

Traditional Requirements Management Tools (Doors, Enterprise Architect, etc):

- Require complex workflows and specific expertise to maintain.
- Many traditional tools can be expensive.
- Cannot be maintained in plain-text alongside the code.

Further Information
-------------------

For more detailed information on using Sphinx-Graph, explore the following sections:

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   src/setup
   src/vertex
   src/table
   src/api
   src/example/index