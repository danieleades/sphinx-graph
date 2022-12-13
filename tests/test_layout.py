import pytest
from sphinx.application import Sphinx
from sphinx.errors import SphinxError


@pytest.mark.sphinx(testroot="layout-unknown")
def test_unknown_layout(app: Sphinx) -> None:
    app.warningiserror = True
    with pytest.raises(
        SphinxError,
        match=r"vertex .* has unknown layout '.*'. Defaulting to '.*' layout.",
    ):
        app.build()
