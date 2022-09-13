import pytest

from sphinx_graph.directives.vertex.directive import parse_parents
from sphinx_graph.directives.vertex.info import Link


@pytest.mark.parametrize("input,expected", [("REQ-01", [Link("REQ-01", None)])])
def test_parse_parents(input: str, expected: list[Link]) -> None:
    output = parse_parents(input)
    assert output == expected
