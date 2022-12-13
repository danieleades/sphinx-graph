import pytest
from sphinx.application import Sphinx
from sphinx.errors import SphinxError

from sphinx_graph.state import DuplicateIdError


@pytest.mark.sphinx(testroot="cycle", freshenv=True)
def test_dependency_cycle(app: Sphinx) -> None:
    app.warningiserror = True
    with pytest.raises(
        SphinxError,
        match=r"vertices must not have cyclic dependencies. cycle detected: .*",
    ):
        app.build()


@pytest.mark.sphinx(testroot="duplicate-ids")
def test_duplicate_ids(app: Sphinx) -> None:
    app.warningiserror = True
    with pytest.raises(DuplicateIdError):
        app.build()
