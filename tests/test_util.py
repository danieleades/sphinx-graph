import pytest

from sphinx_graph.util import unwrap


def test_unwrap_some() -> None:
    x = "string"
    assert unwrap(x) == x


def test_unwrap_none() -> None:
    x = None
    with pytest.raises(
        ValueError,
        match="attempted to 'unwrap' a None value!",
    ):
        unwrap(x)
