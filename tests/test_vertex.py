import pytest
from sphinx.application import Sphinx


@pytest.mark.sphinx(testroot="vertex")
def test_it_builds(app: Sphinx) -> None:
    app.warningiserror = True
    app.build()


@pytest.mark.sphinx(testroot="fingerprints")
def test_require_fingerprints(app: Sphinx) -> None:
    app.warningiserror = True
    app.build()
