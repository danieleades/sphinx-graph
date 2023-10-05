from __future__ import annotations

from contextlib import nullcontext as does_not_raise
from typing import ContextManager

import pytest
from sphinx.errors import ConfigError

from sphinx_graph import parse


@pytest.mark.parametrize(
    ("input", "expected", "expectation"),
    [
        ("true", True, does_not_raise()),
        ("TRUE", True, does_not_raise()),
        ("false", False, does_not_raise()),
        (None, True, does_not_raise()),
        ("test", True, pytest.raises(ConfigError)),
    ],
)
def test_parse_boolean(
    input: str | None,
    expected: bool,
    expectation: ContextManager[None],
) -> None:
    with expectation:
        output = parse.boolean(input)
        assert output == expected


@pytest.mark.parametrize(
    ("input", "expected"),
    [
        (None, {}),
        ("REQ-01", {"REQ-01": None}),
        ("REQ-01:1234", {"REQ-01": "1234"}),
        (
            "REQ-01:1234, REQ-02,REQ-03:5678",
            {"REQ-01": "1234", "REQ-02": None, "REQ-03": "5678"},
        ),
    ],
)
def test_parse_parents(input: str | None, expected: dict[str, str | None]) -> None:
    output = parse.parents(input)
    assert output == expected


@pytest.mark.parametrize(
    ("input", "expected"),
    [
        ("some string", "some string"),
        ("", None),
        (None, None),
    ],
)
def test_parse_str(input: str, expected: str | None) -> None:
    output = parse.string(input)
    assert output == expected


@pytest.mark.parametrize(
    ("input", "expected"),
    [
        (None, []),
        ("one", ["one"]),
        ("one, two", ["one", "two"]),
        ("one,two", ["one", "two"]),
    ],
)
def test_parse_list(input: str, expected: list[str]) -> None:
    output = parse.comma_separated_list(input)
    assert output == expected
