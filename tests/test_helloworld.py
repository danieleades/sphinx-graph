import networkx as nx
import pytest
from sphinx.application import Sphinx

from sphinx_graph.context import DuplicateIdError, get_context
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

    with get_context(unwrap(app.env)) as context:
        assert nx.is_isomorphic(context.graph, graph)
