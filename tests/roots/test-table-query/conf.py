import os
import sys

from sphinx_graph import Config

sys.path.append(os.path.abspath("."))

from queries import family  # noqa: E402

graph_config = Config(queries={"family": family})

extensions = [
    "sphinx_graph",
]
