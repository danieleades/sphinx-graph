import sys
from pathlib import Path

from sphinx_graph import Config

sys.path.append(str(Path().resolve()))

from queries import family  # noqa: E402

graph_config = Config(queries={"family": family})

extensions = [
    "sphinx_graph",
]
