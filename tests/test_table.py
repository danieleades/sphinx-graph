from __future__ import annotations

from typing import Callable
from uuid import uuid4

import pytest
from sphinx.application import Sphinx
from sphinx.errors import ConfigError

from sphinx_graph.table.info import Info
from sphinx_graph.table.state import State
from sphinx_graph.vertex.state import DuplicateIdError


@pytest.mark.sphinx(testroot="table", warningiserror=True)
def test_it_builds(app: Sphinx) -> None:
    app.build()


@pytest.mark.sphinx(testroot="table-query", warningiserror=True)
def test_query_builds(app: Sphinx) -> None:
    app.build()


@pytest.mark.sphinx(testroot="table-query-unknown", warningiserror=True)
def test_query_unknown_fails(app: Sphinx) -> None:
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
        match=r"^Vertex table .* already exists.$",
    ):
        # try to insert an existing uuid
        state.insert(uuid, info=Info(docname="docname", query=None, args={}))


@pytest.mark.sphinx("html")
def test_query_config_isolation(make_app: Callable[..., Sphinx]) -> None:
    from sphinx_graph.vertex import query as query_module

    original = query_module.QUERIES.copy()
    apps: list[Sphinx] = []

    try:
        app = make_app(testroot="table-query")
        apps.append(app)
        app.build()
        assert query_module.QUERIES == original

        app = make_app(testroot="table-query-alt")
        apps.append(app)
        app.build()
        assert query_module.QUERIES == original
    finally:
        for app in apps:
            app.cleanup()
