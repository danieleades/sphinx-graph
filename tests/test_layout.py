import pytest
from sphinx.application import Sphinx


@pytest.mark.sphinx(testroot="layout")
def test_it_builds(app: Sphinx) -> None:
    app.warningiserror = True
    app.build()
