from uuid import uuid4

import pytest
from sphinx.application import Sphinx
from sphinx.errors import ConfigError

from sphinx_graph.table.info import Info
from sphinx_graph.table.state import State
from sphinx_graph.vertex.state import DuplicateIdError


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


def test_duplicate_tables_not_allowed() -> None:
    state = State(tables={})
    uuid = uuid4()

    state.insert(uuid, info=Info(docname="docname", query=None, args={}))

    with pytest.raises(
        DuplicateIdError,
        match="^Vertex table .* already exists.$",
    ):
        # try to insert an existing uuid
        state.insert(uuid, info=Info(docname="docname", query=None, args={}))
