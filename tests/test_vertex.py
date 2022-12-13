import re

import pytest
from sphinx.application import Sphinx
from sphinx.errors import SphinxError


@pytest.mark.sphinx(testroot="vertex")
def test_it_builds(app: Sphinx) -> None:
    app.warningiserror = True
    app.build()


@pytest.mark.sphinx(testroot="fingerprints")
def test_require_fingerprints(app: Sphinx) -> None:
    app.warningiserror = True
    app.build()


@pytest.mark.sphinx(testroot="regex")
def test_regex(app: Sphinx) -> None:
    app.warningiserror = True
    with pytest.raises(
        SphinxError,
        match=re.escape(
            r"vertex '02' doesn't satisfy the configured regex ('^SYS-[0-9]{4}$')"
        ),
    ):
        app.build()
