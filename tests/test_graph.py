import pytest
from sphinx.application import Sphinx
from sphinx.errors import SphinxError
from sphinx_graph.vertex.state import DuplicateIdError, State


@pytest.mark.sphinx(testroot="cycle", freshenv=True)
def test_dependency_cycle(app: Sphinx) -> None:
    app.warningiserror = True
    with pytest.raises(
        SphinxError,
        match=(
            "^vertices must not have cyclic dependencies. cycles detected: \\[REQ-03"
            " -> REQ-01 -> REQ-02 -> REQ-03\\]$"
        ),
    ):
        app.build()


@pytest.mark.sphinx(testroot="duplicate-ids")
def test_duplicate_ids(app: Sphinx) -> None:
    app.warningiserror = True
    with pytest.raises(DuplicateIdError):
        app.build()


@pytest.mark.sphinx(testroot="vertex")
def test_vertices(app: Sphinx) -> None:
    app.warningiserror = True
    app.build()
    state = State.read(app.env)
    expected_len = 5
    assert len(state.vertices) == expected_len
    assert len(state.node_ids) == expected_len
