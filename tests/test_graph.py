import pytest
from sphinx.application import Sphinx
from sphinx.errors import SphinxError

from sphinx_graph.vertex.state import DuplicateIdError, State


@pytest.mark.sphinx(
    testroot="cycle", freshenv=True, warningiserror=True, exception_on_warning=True
)
def test_dependency_cycle(app: Sphinx) -> None:
    with pytest.raises(
        SphinxError,
        match=(
            r"^vertices must not have cyclic dependencies. cycles detected: \[REQ-03"
            r" -> REQ-01 -> REQ-02 -> REQ-03\]$"
        ),
    ):
        app.build()


@pytest.mark.sphinx(testroot="duplicate-ids", warningiserror=True)
def test_duplicate_ids(app: Sphinx) -> None:
    with pytest.raises(DuplicateIdError):
        app.build()


@pytest.mark.sphinx(testroot="vertex", warningiserror=True)
def test_vertices(app: Sphinx) -> None:
    app.build()
    state = State.read(app.env)
    expected_len = 5
    assert len(state.vertices) == expected_len
    assert len(state.node_ids) == expected_len


@pytest.mark.sphinx(
    testroot="missing-required-parent",
    freshenv=True,
    warningiserror=True,
    exception_on_warning=True,
)
def test_missing_required_parent(app: Sphinx) -> None:
    with pytest.raises(
        SphinxError,
        match=(
            r"vertex 'SYS-002' is required to have at least one parent but has none"
        ),
    ):
        app.build()
