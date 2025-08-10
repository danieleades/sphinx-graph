import re

import pytest
from sphinx.application import Sphinx
from sphinx.errors import SphinxError

from sphinx_graph import vertex


@pytest.mark.sphinx(testroot="vertex", warningiserror=True)
def test_it_builds(app: Sphinx) -> None:
    app.build()


@pytest.mark.sphinx(testroot="parallel", parallel=2, warningiserror=True)
def test_it_builds_parallel(app: Sphinx) -> None:
    app.build()


@pytest.mark.sphinx(testroot="fingerprints", warningiserror=True)
def test_require_fingerprints(app: Sphinx) -> None:
    app.build()


@pytest.mark.sphinx(
    testroot="missing-fingerprint", warningiserror=True, exception_on_warning=True
)
def test_missing_fingerprint(app: Sphinx) -> None:
    with pytest.raises(
        SphinxError,
        match=(
            r"^link fingerprints are required, but [0-9]+ doesn't have a fingerprint"
            " for its link to its parent"
        ),
    ):
        app.build()


@pytest.mark.sphinx(
    testroot="incorrect-fingerprint", warningiserror=True, exception_on_warning=True
)
def test_incorrect_fingerprint(app: Sphinx) -> None:
    with pytest.raises(
        SphinxError,
        match=(
            r"suspect link found. vertex ([0-9]+) is linked to vertex ([0-9]+) with a"
            r" fingerprint of 'abcd', but \2's fingerprint is '[\S]{4}'.\n\1 should be"
            " reviewed, and the link fingerprint manually updated."
        ),
    ):
        app.build()


@pytest.mark.sphinx(testroot="regex", warningiserror=True)
def test_regex(app: Sphinx) -> None:
    with pytest.raises(
        SphinxError,
        match=re.escape(
            r"vertex '02' doesn't satisfy the configured regex ('^SYS-[0-9]{4}$')",
        ),
    ):
        app.build()


@pytest.mark.sphinx(testroot="tags", warningiserror=True)
def test_tags_builds(app: Sphinx) -> None:
    app.build()

    state = vertex.State.read(app.env)
    assert state.vertices["01"].tags == ["P1", "component::x", "milestone::a"]


@pytest.mark.sphinx(testroot="invalid-parent", warningiserror=True)
def test_invalid_parent(app: Sphinx) -> None:
    with pytest.raises(
        SphinxError,
        match=r"^vertex '02' has a parent link to '03', but '03' doesn't exist$",
    ):
        app.build()
