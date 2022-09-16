"""Custom configuration for Sphinx Graph."""

from dataclasses import dataclass


@dataclass
class Config:
    """Configuration object for Sphinx Graph.

    This class is the entry point for all configuration.

    Example:
        Configuration should be set in the ``conf.py`` file:

        .. code:: python

            from sphinx_graph import Config

            sphinx_config = Config(
                require_fingerprints=True,
            )


    Args:
        require_fingerprints:
            Whether parent links *must* provide fingerprints.
            If ``False`` (the default) then link fingerprints are checked
            if set, and ignored otherwise.
    """

    require_fingerprints: bool = False
