.. example-basic documentation master file, created by
   sphinx-quickstart on Mon Sep  5 06:01:44 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Basic Example
=============

.. toctree::
   :maxdepth: 2
   :caption: Contents:


.. vertex:: 01
   :children: 04

   this is a vertex directive

.. vertex:: 02
   :parents: 01

   this is a vertex directive

.. vertex:: 03
   :parents: 01

   this is a vertex directive

.. vertex:: 04

   this is a vertex directive

.. vertex:: 05

   this is a vertex directive



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
