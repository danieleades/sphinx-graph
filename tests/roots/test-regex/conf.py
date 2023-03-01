import re

from sphinx_graph import Config, VertexConfig

extensions = [
    "sphinx_graph",
]

graph_config = Config(
    types={
        "usr": VertexConfig(regex=re.compile(r"^USR-[0-9]{4}$")),
        "sys": VertexConfig(regex=re.compile(r"^SYS-[0-9]{4}$")),
    },
)
