from __future__ import annotations

import pytest

from sphinx_graph.directives.vertex.directive import parse_parents, parse_str
from sphinx_graph.directives.vertex.info import Link


@pytest.mark.parametrize(
    "input,expected",
    [
        ("REQ-01", [Link("REQ-01", None)]),
        ("REQ-01:1234", [Link("REQ-01", "1234")]),
        (
            "REQ-01:1234, REQ-02,REQ-03:5678",
            [Link("REQ-01", "1234"), Link("REQ-02", None), Link("REQ-03", "5678")],
        ),
    ],
)
def test_parse_parents(input: str, expected: list[Link]) -> None:
    output = parse_parents(input)
    assert output == expected


@pytest.mark.parametrize(
    "input,expected",
    [
        ("some string", "some string"),
        ("", None),
        (None, None),
    ],
)
def test_parse_str(input: str, expected: str | None) -> None:
    output = parse_str(input)
    assert output == expected
