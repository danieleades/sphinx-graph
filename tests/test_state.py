from sphinx_graph.vertex.config import Config
from sphinx_graph.vertex.info import Info
from sphinx_graph.vertex.state import NodeIds


def test_state() -> None:
    vertices: dict[str, tuple[int, Info]] = {
        "01": (
            1,
            Info("docname", Config(), parents={}, fingerprint="fingerprint", tags=[]),
        )
    }

    node_ids = NodeIds(vertices)

    assert list(iter(node_ids)) == ["01"]
