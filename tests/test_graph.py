import pytest
from sphinx.application import Sphinx
from sphinx.errors import SphinxError

from sphinx_graph.vertex.state import DuplicateIdError


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


@pytest.mark.sphinx(testroot="missing-fingerprint")
def test_missing_fingerprint(app: Sphinx) -> None:
    app.warningiserror = True
    with pytest.raises(
        SphinxError,
        match=(
            r"^link fingerprints are required, but [0-9]+ doesn't have a fingerprint"
            " for its link to its parent"
        ),
    ):
        app.build()


@pytest.mark.sphinx(testroot="incorrect-fingerprint")
def test_incorrect_fingerprint(app: Sphinx) -> None:
    app.warningiserror = True
    with pytest.raises(
        SphinxError,
        match=(
            r"suspect link found. vertex ([0-9]+) is linked to vertex ([0-9]+) with a"
            r" fingerprint of 'abcd', but \2's fingerprint is '[\S]{4}'.\n\1 should be"
            " reviewed, and the link fingerprint manually updated."
        ),
    ):
        app.build()
