import pytest
from sphinx.application import Sphinx
from sphinx.errors import SphinxError

from sphinx_graph.vertex.state import DuplicateIdError


@pytest.mark.sphinx(testroot="cycle", freshenv=True)
def test_dependency_cycle(app: Sphinx) -> None:
    app.warningiserror = True
    with pytest.raises(
        SphinxError,
        match=r"^vertices must not have cyclic dependencies. cycles detected: ",
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
            r"suspect link found. vertex 02 is linked to vertex 01 with a fingerprint"
            " of 'abcd', but 01's fingerprint is '/470'.\n02 should be reviewed, and"
            " the link fingerprint manually updated."
        ),
    ):
        app.build()
