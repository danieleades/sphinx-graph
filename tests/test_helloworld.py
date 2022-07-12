import pytest
from sphinx.application import Sphinx

from sphinx_graph.context import DuplicateIdError


@pytest.mark.sphinx(testroot="vertex")
def test_vertex(app: Sphinx) -> None:
    app.warningiserror = True
    app.build()


@pytest.mark.sphinx(testroot="duplicate-ids")
def test_duplicate_ids(app: Sphinx) -> None:
    app.warningiserror = True
    with pytest.raises(DuplicateIdError):
        app.build()
