from __future__ import annotations

from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest
from sphinx.errors import ConfigError
from sphinx_graph import parse


@pytest.mark.parametrize(
    ("value", "expected", "expectation"),
    [
        ("true", True, does_not_raise()),
        ("TRUE", True, does_not_raise()),
        ("false", False, does_not_raise()),
        (None, True, does_not_raise()),
        ("test", True, pytest.raises(ConfigError)),
    ],
)
def test_parse_boolean(
    value: str | None,
    expected: bool,  # noqa: FBT001
    expectation: AbstractContextManager[None],
) -> None:
    with expectation:
        output = parse.boolean(value)
        assert output == expected


@pytest.mark.parametrize(
    ("value", "expected"),
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
def test_parse_parents(value: str | None, expected: dict[str, str | None]) -> None:
    output = parse.parents(value)
    assert output == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("some string", "some string"),
        ("", None),
        (None, None),
    ],
)
def test_parse_str(value: str, expected: str | None) -> None:
    output = parse.string(value)
    assert output == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, []),
        ("one", ["one"]),
        ("one, two", ["one", "two"]),
        ("one,two", ["one", "two"]),
    ],
)
def test_parse_list(value: str, expected: list[str]) -> None:
    output = parse.comma_separated_list(value)
    assert output == expected
