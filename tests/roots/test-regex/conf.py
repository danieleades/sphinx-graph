import re

from sphinx_graph import Config, VertexConfig

project = "test"
copyright = "2022, daniel.eades"
author = "daniel.eades"


extensions = [
    "sphinx_graph",
]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

graph_config = Config(
    types={
        "usr": VertexConfig(regex=re.compile(r"^USR-[0-9]{4}$")),
        "sys": VertexConfig(regex=re.compile(r"^SYS-[0-9]{4}$")),
    },
)
