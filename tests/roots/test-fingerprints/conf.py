from sphinx_graph import Config, VertexConfig

extensions = [
    "sphinx_graph",
]


graph_config = Config(
    vertex_config=VertexConfig(require_fingerprints=True),
    types={
        "req": VertexConfig(
            require_fingerprints=False,
        )
    },
)
