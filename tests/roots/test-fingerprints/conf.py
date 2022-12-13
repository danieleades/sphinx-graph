from sphinx_graph import Config, VertexConfig

project = "test"
copyright = "2022, daniel.eades"
author = "daniel.eades"

extensions = [
    "sphinx_graph",
]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

graph_config = Config(
    vertex_config=VertexConfig(require_fingerprints=True),
    types={
        "req": VertexConfig(
            require_fingerprints=False,
        )
    },
)
