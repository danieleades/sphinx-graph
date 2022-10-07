"""Custom configuration for Sphinx Graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sphinx_graph.vertex.layout import Formatter


@dataclass
class Config:
    """Configuration object for Sphinx Graph.

    This class is the entry point for all configuration.

    Example:
        Configuration should be set in the ``conf.py`` file:

        .. code:: python

            from sphinx_graph import Config

            graph_config = Config(
                require_fingerprints=True,
            )


    Args:
        require_fingerprints:
            Whether parent links *must* provide fingerprints.
            If ``False`` (the default) then link fingerprints are checked
            if set, and ignored otherwise.
        custom_layouts:
            Optionally add additional custom layouts that can be used by Vertices.

            Eg:

            .. code:: python

                from sphinx_graph import Config, FormatHelper

                # -------------------------------------------------------------
                # this function must be defined in a separate file, otherwise Sphinx cannot 'pickle' the config!
                def format_custom(helper: FormatHelper) -> Sequence[nodes.Node]:
                    line_block = nodes.line_block()

                    line_block += nodes.line("", f"UID: {helper.uid}")

                    if helper.parents:
                        line_block += helper.parent_list()

                    if helper.children:
                        line_block += helper.child_list()

                    return [line_block, helper.content]
                # -------------------------------------------------------------

                graph_config = Config(
                    custom_layouts={
                        "custom": format_custom
                    },
                )
    """

    require_fingerprints: bool = False
    custom_layouts: dict[str, Formatter] = field(default_factory=dict)
