"""Types and methods specific to the vertex-table directive."""

from .directive import Directive
from .info import Info
from .node import TableNode
from .registration import register

__all__ = [
    "Directive",
    "Info",
    "TableNode",
    "register",
]
