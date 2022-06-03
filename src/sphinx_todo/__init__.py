"""Entrypoint for the sphinx-todo extension."""

from dataclasses import dataclass
from typing import List, Sequence, TypedDict

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective

from sphinx_todo.config import Config as TodoConfig
from sphinx_todo.util import unwrap

__all__ = [
    "TodoConfig",
]


class ToDo(nodes.Admonition, nodes.Element):
    """An RST node representing a To-Do item."""

    pass


class ToDoList(nodes.General, nodes.Element):
    """An RST node representing a list of To-Do items."""

    pass


def visit_todo_node(self: nodes.GenericNodeVisitor, node: ToDo) -> None:
    self.visit_admonition(node)  # type: ignore[attr-defined]


def depart_todo_node(self: nodes.GenericNodeVisitor, node: ToDo) -> None:
    self.depart_admonition(node)  # type: ignore[attr-defined]


class TodolistDirective(Directive):
    """An RST directive which produces a To-Do list node."""

    def run(self) -> List[ToDoList]:
        """Run the directive and return a ToDoList node."""
        return [ToDoList("")]


@dataclass
class TodoInfo:
    docname: str
    lineno: int
    todo: ToDo
    target: nodes.target


class TodoDirective(SphinxDirective):
    """An RST directive which produces a To-Do node."""

    # this enables content in the directive
    has_content = True

    def run(self) -> Sequence[nodes.Node]:
        """Run the directive and return a ToDo node."""
        todo_all_todos: List[TodoInfo] = getattr(self.env, "todo_all_todos", [])

        targetid = f"todo-{self.env.new_serialno('todo')}"
        targetnode = nodes.target("", "", ids=[targetid])

        todo_node = ToDo("\n".join(self.content))
        todo_node += nodes.title(_("Todo"), _("Todo"))
        self.state.nested_parse(self.content, self.content_offset, todo_node)

        todo_all_todos.append(
            TodoInfo(
                docname=self.env.docname,
                lineno=self.lineno,
                todo=todo_node.deepcopy(),
                target=targetnode,
            )
        )

        self.env.todo_all_todos = todo_all_todos  # type: ignore[attr-defined]

        return [targetnode, todo_node]


def purge_todos(_app: Sphinx, env: BuildEnvironment, docname: str) -> None:
    """
    Clear out all todos whose docname matches the given one from the todo_all_todos list.

    If there are todos left in the document, they will be added again during parsing.
    """
    todo_all_todos: List[TodoInfo] = getattr(env, "todo_all_todos", [])

    todo_all_todos = [todo for todo in todo_all_todos if todo.docname != docname]
    env.todo_all_todos = todo_all_todos  # type: ignore[attr-defined]


def merge_todos(
    _app: Sphinx, env: BuildEnvironment, _docnames: List[str], other: BuildEnvironment
) -> None:
    """Merge the todos from multiple environments during parallel builds."""
    todo_all_todos: List[TodoInfo] = getattr(env, "todo_all_todos", [])
    todo_all_todos.extend(getattr(other, "todo_all_todos", []))

    env.todo_all_todos = todo_all_todos  # type: ignore[attr-defined]


def process_todo_nodes(app: Sphinx, doctree: nodes.document, fromdocname: str) -> None:
    config: TodoConfig = app.config.todo_config
    if not config.include_todos:
        for todo_node in doctree.findall(ToDo):
            todo_node.parent.remove(todo_node)

    # Replace all ToDoList nodes with a list of the collected todos.
    # Augment each todo with a backlink to the original location.
    builder = unwrap(app.builder)
    env = unwrap(builder.env)

    # get the list of todos from the environment
    todo_all_todos: List[TodoInfo] = getattr(env, "todo_all_todos", [])

    for todolist_node in doctree.findall(ToDoList):
        if not config.include_todos:
            todolist_node.replace_self([])
            continue

        content: List[nodes.Node] = []

        for todo_info in todo_all_todos:
            para = nodes.paragraph()
            filename = env.doc2path(todo_info.docname, base=False)
            description = _(
                f"(The original entry is located in {filename},"
                f" line {todo_info.lineno} and can be found "
            )
            para += nodes.Text(description)

            # Create a reference
            newnode = nodes.reference("", "")
            innernode = nodes.emphasis(_("here"), _("here"))
            newnode["refdocname"] = todo_info.docname
            newnode["refuri"] = builder.get_relative_uri(fromdocname, todo_info.docname)
            newnode["refuri"] += f"#{todo_info.target['refid']}"
            newnode.append(innernode)
            para += newnode
            para += nodes.Text(".)")

            # Insert into the ToDoList
            content.append(todo_info.todo)
            content.append(para)

        todolist_node.replace_self(content)

    # update the environment with the latest todos
    env.todo_all_todos = todo_all_todos  # type: ignore[attr-defined]


class ExtensionMetadata(TypedDict):
    version: str
    env_version: int
    parallel_read_safe: bool
    parallel_write_safe: bool


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_config_value("todo_config", TodoConfig(), "", types=(TodoConfig))

    app.add_node(ToDoList)
    app.add_node(
        ToDo,
        html=(visit_todo_node, depart_todo_node),
        latex=(visit_todo_node, depart_todo_node),
        text=(visit_todo_node, depart_todo_node),
    )

    app.add_directive("todo", TodoDirective)
    app.add_directive("todolist", TodolistDirective)
    app.connect("doctree-resolved", process_todo_nodes)
    app.connect("env-purge-doc", purge_todos)
    app.connect("env-merge-info", merge_todos)

    return {
        "version": "0.1",
        "env_version": 0,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
