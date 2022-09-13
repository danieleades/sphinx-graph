import networkx as nx
import pytest
from sphinx.application import Sphinx
from sphinx.errors import SphinxError, SphinxWarning

from sphinx_graph.directives.vertex.state import DuplicateIdError, get_state
from sphinx_graph.util import unwrap


@pytest.mark.sphinx(testroot="vertex")
def test_it_builds(app: Sphinx) -> None:
    app.warningiserror = True
    app.build()


@pytest.mark.sphinx(testroot="duplicate-ids")
def test_duplicate_ids(app: Sphinx) -> None:
    app.warningiserror = True
    with pytest.raises(DuplicateIdError):
        app.build()


@pytest.mark.sphinx(testroot="vertex", freshenv=True)
def test_graph(app: Sphinx) -> None:
    app.warningiserror = True
    app.build()

    graph = nx.DiGraph()
    graph.add_edge("02", "01")
    graph.add_edge("03", "01")
    graph.add_edge("04", "01")
    graph.add_node("05")

    with get_state(unwrap(app.env)) as state:
        assert nx.is_isomorphic(state.graph, graph)


@pytest.mark.sphinx(testroot="fingerprints", freshenv=True)
def test_fingerprints(app: Sphinx) -> None:
    app.warningiserror = True
    app.build()


@pytest.mark.sphinx(testroot="fingerprints-missing", freshenv=True)
def test_fingerprints_missing(app: Sphinx) -> None:
    app.warningiserror = True
    with pytest.raises(SphinxWarning):
        app.build()


@pytest.mark.sphinx(testroot="fingerprints-wrong", freshenv=True)
def test_fingerprints_wrong(app: Sphinx) -> None:
    app.warningiserror = True
    with pytest.raises(SphinxWarning):
        app.build()


@pytest.mark.sphinx(testroot="cycle", freshenv=True)
def test_dependency_cycle(app: Sphinx) -> None:
    app.warningiserror = True
    with pytest.raises(
        SphinxError,
        match=r"vertices must not have cyclic dependencies. cycle detected: .*",
    ):
        app.build()
