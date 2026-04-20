from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from docutils import nodes
from sphinx.errors import SphinxError

from sphinx_graph import formatting

if TYPE_CHECKING:
    from sphinx.application import Sphinx


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ([], []),
        ([nodes.Text("A")], [nodes.Text("A")]),
        (
            [nodes.Text("A"), nodes.Text("B"), nodes.Text("C")],
            [
                nodes.Text("A"),
                nodes.Text(", "),
                nodes.Text("B"),
                nodes.Text(", "),
                nodes.Text("C"),
            ],
        ),
    ],
)
def test_comma_separated_list(
    value: list[nodes.Node],
    expected: list[nodes.Node],
) -> None:
    output = list(formatting.comma_separated_list(value))
    assert output == expected


@pytest.mark.sphinx(
    testroot="layout-unknown", warningiserror=True, exception_on_warning=True
)
def test_unknown_layout(app: Sphinx) -> None:
    with pytest.raises(
        SphinxError,
        match=r"vertex .* has unknown layout '.*'. Defaulting to '.*' layout.",
    ):
        app.build()


@pytest.mark.sphinx(testroot="vertex", buildername="html", warningiserror=True)
def test_subtle_layout_html(app: Sphinx) -> None:
    """The subtle layout emits an inline span that wraps naturally in HTML."""
    app.build()

    output = (Path(app.outdir) / "index.html").read_text()

    assert 'class="sphinx-graph-subtle"' in output
    assert "<sub>" not in output


@pytest.mark.sphinx(testroot="vertex", buildername="latex", warningiserror=True)
def test_subtle_layout_latex(app: Sphinx) -> None:
    r"""The subtle layout emits a DUrole whose LaTeX macro uses \textsubscript.

    \textsubscript is text-mode, so long parent/child lists wrap across lines
    in the PDF output. Math-mode subscript ($_{...}$) would not wrap.
    """
    app.build()

    tex_files = list(Path(app.outdir).glob("*.tex"))
    assert tex_files, "expected a .tex file in the build output"
    output = tex_files[0].read_text()

    assert r"\DUrole{sphinx-graph-subtle}" in output
    assert (
        r"\expandafter\providecommand\csname DUrolesphinx-graph-subtle\endcsname"
        in output
    )
    assert r"\textsubscript" in output
