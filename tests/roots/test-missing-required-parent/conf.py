from sphinx_graph import Config, VertexConfig

extensions = [
    "sphinx_graph",
]


graph_config = Config(
    types={
        "usr": VertexConfig(),
        "sys": VertexConfig(require_parent=True),
    },
)
