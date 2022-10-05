from typing import Sequence
from sphinx_graph import FormatHelper
from docutils import nodes


def format_custom(helper: FormatHelper) -> Sequence[nodes.Node]:
    line_block = nodes.line_block()

    line_block += nodes.line("", f"UID: {helper.uid}")

    if helper.parents:
        line_block += helper.parent_list()

    if helper.children:
        line_block += helper.child_list()

    return [line_block, helper.content]
