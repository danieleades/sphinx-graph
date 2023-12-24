import sys
from pathlib import Path

from sphinx_graph import Config

sys.path.append(str(Path.cwd()))

from queries import family

graph_config = Config(queries={"family": family})

extensions = [
    "sphinx_graph",
]
