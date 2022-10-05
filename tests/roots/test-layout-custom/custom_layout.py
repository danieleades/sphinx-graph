from typing import Sequence

from docutils import nodes

from sphinx_graph import FormatHelper


def format_custom(helper: FormatHelper) -> Sequence[nodes.Node]:
    line_block = nodes.line_block()

    line_block += nodes.line("", f"UID: {helper.uid}")

    if helper.parents:
        line_block += helper.parent_list()

    if helper.children:
        line_block += helper.child_list()

    return [line_block, helper.content]
