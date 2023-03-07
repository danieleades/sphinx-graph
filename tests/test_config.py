from sphinx_graph import vertex


def test_vertex_config_override_fingerprints() -> None:
    default_config = vertex.Config(require_fingerprints=True)
    type_config = vertex.Config()
    directive_config = vertex.Config()

    vertex_config = default_config.override(type_config).override(directive_config)

    assert vertex_config.require_fingerprints
