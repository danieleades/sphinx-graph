import pytest

from sphinx_graph import util


def test_unwrap() -> None:
    input = "input"
    expected = "input"

    assert util.unwrap(input) == expected

    with pytest.raises(ValueError):
        util.unwrap(None)
