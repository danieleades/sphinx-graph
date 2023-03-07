import pytest
from sphinx.application import Sphinx
from sphinx.errors import ConfigError


@pytest.mark.sphinx(testroot="table")
def test_it_builds(app: Sphinx) -> None:
    app.warningiserror = True
    app.build()


@pytest.mark.sphinx(testroot="table-query")
def test_query_builds(app: Sphinx) -> None:
    app.warningiserror = True
    app.build()


@pytest.mark.sphinx(testroot="table-query-unknown")
def test_query_unknown_fails(app: Sphinx) -> None:
    app.warningiserror = True
    with pytest.raises(
        ConfigError,
        match="no query registered with name 'unknown'",
    ):
        app.build()
