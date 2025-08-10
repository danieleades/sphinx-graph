from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from docutils import nodes
from sphinx.errors import SphinxError

from sphinx_graph import formatting

if TYPE_CHECKING:
    from sphinx.application import Sphinx


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ([], []),
        ([nodes.Text("A")], [nodes.Text("A")]),
        (
            [nodes.Text("A"), nodes.Text("B"), nodes.Text("C")],
            [
                nodes.Text("A"),
                nodes.Text(", "),
                nodes.Text("B"),
                nodes.Text(", "),
                nodes.Text("C"),
            ],
        ),
    ],
)
def test_comma_separated_list(
    value: list[nodes.Node],
    expected: list[nodes.Node],
) -> None:
    output = list(formatting.comma_separated_list(value))
    assert output == expected


@pytest.mark.sphinx(
    testroot="layout-unknown", warningiserror=True, exception_on_warning=True
)
def test_unknown_layout(app: Sphinx) -> None:
    with pytest.raises(
        SphinxError,
        match=r"vertex .* has unknown layout '.*'. Defaulting to '.*' layout.",
    ):
        app.build()
