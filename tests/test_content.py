import pytest
from sphinx.application import Sphinx


@pytest.mark.sphinx(testroot="nested-headers")
def test_nested_headers(app: Sphinx) -> None:
    app.warningiserror = True
    app.build()
