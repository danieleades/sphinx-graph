"""Sphinx Directive for Vertex objects."""

from dataclasses import dataclass, field
from typing import Iterator, List, Sequence

from docutils import nodes
from sphinx.builders import Builder
from sphinx.util.docutils import SphinxDirective

from sphinx_graph import parse
from sphinx_graph.directives.vertex.info import Info, InfoParsed
from sphinx_graph.directives.vertex.node import Node
from sphinx_graph.directives.vertex.state import State, get_state
from sphinx_graph.util import comma_separated_list

__all__ = [
    "Directive",
]


@dataclass
class Args:
    """Parsed arguments for the Vertex directive."""

    uid: str
    parents: List[str] = field(default_factory=list)


class Directive(SphinxDirective):
    """An RST node representing a To-Do item."""

    has_content = True
    required_arguments = 1
    option_spec = {
        "parents": parse.list,
    }

    def run(self) -> Sequence[nodes.Node]:
        """Run the directive and return a Vertex node."""
        args = Args(uid=self.arguments[0], **self.options)

        content_node = Node("\n".join(self.content))
        self.state.nested_parse(self.content, self.content_offset, content_node)

        targetnode = nodes.target("", "", ids=[args.uid])
        placeholder_node = Node(ids=[args.uid])

        with get_state(self.env) as state:
            state.insert_vertex(
                args.uid,
                Info(
                    docname=self.env.docname,
                    lineno=self.lineno,
                    node=content_node,
                    target=targetnode,
                    parents=args.parents,
                ),
            )

        return [targetnode, placeholder_node]


def format_reference(id: str, reference: nodes.reference) -> nodes.reference:
    reference.append(nodes.Text(id))
    return reference


def create_references(
    state: State, builder: Builder, from_docname: str, ids: list[str]
) -> Iterator[nodes.Node]:
    for id in ids:
        reference = format_reference(
            id, state.create_reference(builder, id, from_docname)
        )
        yield reference


def create_references_para(
    state: State, builder: Builder, from_docname: str, prefix: str, ids: list[str]
) -> nodes.paragraph:
    references = list(create_references(state, builder, from_docname, ids))
    if references:
        para = nodes.paragraph()
        para += nodes.Text(prefix)
        para.extend(comma_separated_list(references))
        return para
    return None


def format_node(state: State, builder: Builder, info: InfoParsed) -> nodes.Node:
    """Generate a formatted vertex, ready for insertion into the document."""
    table: nodes.Node = nodes.table()
    tgroup = nodes.tgroup(cols=1)
    colspec = nodes.colspec(colwidth=1)
    tgroup.append(colspec)
    table += tgroup

    # add header
    thead = nodes.thead()
    tgroup += thead
    row = nodes.row()
    entry = nodes.entry()
    entry += nodes.paragraph(text=f"Requirement: {info.id}")
    row += entry
    thead.append(row)

    tbody = nodes.tbody()

    # add attributes
    row = nodes.row()
    entry = nodes.entry()

    for prefix, ids in [("parents: ", info.parents), ("children: ", info.children)]:
        para = create_references_para(state, builder, info.docname, prefix, ids)
        if para:
            entry += para

    row += entry
    tbody.append(row)

    # add content
    row = nodes.row()
    entry = nodes.entry()
    entry += info.node
    row += entry

    tbody.append(row)

    tgroup += tbody

    return table
