import pytest
from docutils import nodes

from sphinx_graph import util


@pytest.mark.parametrize(
    "input,expected",
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
    input: list[nodes.Node], expected: list[nodes.Node]
) -> None:
    output = list(util.comma_separated_list(input))
    assert output == expected
