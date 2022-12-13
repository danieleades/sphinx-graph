from sphinx_graph import VertexConfig


def test_vertex_config_override_fingerprints() -> None:
    default_config = VertexConfig(require_fingerprints=True)
    type_config = VertexConfig()
    directive_config = VertexConfig()

    vertex_config = default_config._override(type_config)._override(directive_config)

    assert vertex_config.require_fingerprints
