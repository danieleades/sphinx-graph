import pytest
from sphinx.application import Sphinx


@pytest.mark.sphinx(testroot="vertex")
def test_vertex(app: Sphinx) -> None:
    app.build()
