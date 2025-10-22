import sys
from pathlib import Path

from sphinx_graph import Config

sys.path.append(str(Path.cwd()))

from queries import siblings

graph_config = Config(queries={"siblings": siblings})

extensions = [
    "sphinx_graph",
]
