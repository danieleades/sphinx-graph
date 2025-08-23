from __future__ import annotations

import rustworkx as rx

from sphinx_graph.vertex.config import Config as VertexConfig
from sphinx_graph.vertex.info import Info
from sphinx_graph.vertex.state import State as VertexState
from sphinx_graph.vertex.state import build_graph_edges


def test_children_returns_uids() -> None:
    # Build a tiny graph: P -> C
    graph: rx.PyDiGraph[str, str | None] = rx.PyDiGraph()
    p_id = graph.add_node("P")
    c_id = graph.add_node("C")

    vertices: dict[str, tuple[int, Info]] = {
        "P": (
            p_id,
            Info(
                docname="doc",
                config=VertexConfig(),
                parents={},
                fingerprint="fpP",
                tags=[],
            ),
        ),
        "C": (
            c_id,
            Info(
                docname="doc",
                config=VertexConfig(),
                parents={"P": None},
                fingerprint="fpC",
                tags=[],
            ),
        ),
    }

    build_graph_edges(vertices, graph)
    state = VertexState(vertices, graph)

    assert list(state.children("P")) == ["C"]
    assert list(state.children("C")) == []
