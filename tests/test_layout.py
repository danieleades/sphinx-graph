from __future__ import annotations

import pytest
from docutils import nodes
from sphinx.application import Sphinx
from sphinx.errors import SphinxError

from sphinx_graph import format


@pytest.mark.parametrize(
    ("input", "expected"),
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
    input: list[nodes.Node],
    expected: list[nodes.Node],
) -> None:
    output = list(format.comma_separated_list(input))
    assert output == expected


@pytest.mark.sphinx(testroot="layout-unknown")
def test_unknown_layout(app: Sphinx) -> None:
    app.warningiserror = True
    with pytest.raises(
        SphinxError,
        match=r"vertex .* has unknown layout '.*'. Defaulting to '.*' layout.",
    ):
        app.build()
