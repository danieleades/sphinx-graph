import sys
from pathlib import Path

from sphinx_graph import Config

<<<<<<< HEAD
sys.path.append(str(Path.cwd()))
=======
sys.path.append(str(Path().cwd()))
>>>>>>> 403eb08 (drop support for python 3.8)

from queries import family  # noqa: E402

graph_config = Config(queries={"family": family})

extensions = [
    "sphinx_graph",
]
