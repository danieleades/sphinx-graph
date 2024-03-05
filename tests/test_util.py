import pytest
from sphinx_graph import util


def test_unwrap() -> None:
    value = "input"
    expected = "input"

    assert util.unwrap(value) == expected

    with pytest.raises(
        ValueError,
        match="attempted to 'unwrap' a None value!",
    ):
        util.unwrap(None)
