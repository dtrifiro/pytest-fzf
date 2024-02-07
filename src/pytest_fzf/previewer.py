from __future__ import annotations

import ast
import os
import sys

import pygments
import pygments.formatters
import pygments.lexers
from pygments.styles import get_style_by_name

LEXER = pygments.lexers.PythonLexer()


def _get_formatter() -> pygments.formatter.Formatter:
    style = os.getenv("PYTEST_FZF_THEME") or os.getenv("BAT_THEME")

    if not style:
        return pygments.formatters.TerminalTrueColorFormatter()

    try:
        return pygments.formatters.TerminalTrueColorFormatter(
            style=get_style_by_name(style),
        )
    except pygments.util.ClassNotFound:
        import warnings

        warnings.warn(
            f'Could not find pygments style: "{style}", falling back to default.',
            stacklevel=0,
        )
        return pygments.formatters.TerminalTrueColorFormatter()


def highlight(
    code: str,
) -> str:
    return pygments.highlight(
        code,
        lexer=LEXER,
        formatter=_get_formatter(),
    )


def usage() -> None:
    command = os.path.basename(sys.argv[0])  # noqa: PTH119
    print(
        "Usage: \n"
        f"  {command} [<nodespec> | <path/to/file.py>"
        "<object name> [expected_parent_name]]\n"
        "\nWhere nodespec is a pytest nodespec: path/to/test_module.py::test_name"
        " or path/to/test_module.py::class_name::test_name"
        "\n"
        "Example:\n"
        "  pytest-fzf-preview tests/test_previewer.py::test_previewer_theme_default\n"
        "  pytest-fzf-preview tests/test_previewer.py",
        file=sys.stderr,
    )


def parse_nodespec(nodespec: str) -> tuple[str, str | None, str, list[str]]:
    """Parse file name and test name from pytest nodespec.

    pytest nodespec: `path/to/test_module.py::class_name::test_name`

    class name is optional
    """
    if "[" in nodespec:
        nodespec, params_str = nodespec.split("[", maxsplit=1)

        params = (
            params_str[:-1].split(",")  # remove the trailing ]
            if params_str
            else []
        )
    else:
        params = []

    file, rest = nodespec.split("::", maxsplit=1)
    if "::" in rest:
        class_name, test_name = rest.split("::")
    else:
        test_name = rest
        class_name = None

    return file, class_name, test_name, params


def _parse_args(argv: list[str]) -> tuple[str, str | None, str | None]:
    """Parse file name, and object name from cmdline."""
    file: str
    object_name: str | None
    expected_parent_name: str | None

    if "::" in argv[1]:
        file, class_name, object_name, _ = parse_nodespec(argv[1])

        expected_parent_name = class_name
        return file, object_name, expected_parent_name

    file = argv[1]  # path to file
    object_name = argv[2] if argv[2:] else None
    expected_parent_name = argv[3] if argv[3:] else None
    return file, object_name, expected_parent_name


def print_highlighted(source: str, start_line: int = 1) -> None:
    """Print the given source with syntax highlighting and line numbers."""
    lines = highlight(source).strip().split("\n")
    max_lineno_width = len(str(len(lines)))

    line_formatter = f"{{lineno:{max_lineno_width}d}}"
    for index, line in enumerate(lines):
        line_no = line_formatter.format(lineno=start_line + index)
        print(f"{line_no} │ {line}")


def cli() -> None:
    if not sys.argv[1:]:
        usage()
        sys.exit(1)

    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        usage()
        sys.exit(0)

    file, object_name, parent_name = _parse_args(sys.argv)
    try:
        with open(file) as fh:
            source = fh.read()
    except FileNotFoundError:
        print(f"File not found: {file}", file=sys.stderr)
        sys.exit(1)

    if not object_name:
        with open(file) as fh:
            print_highlighted(fh.read())
        sys.exit(0)

    res = get_source_for_object(
        source,
        object_name=object_name,
    )
    if not res:
        print(
            f"Could not find `{object_name}` in "
            + (file if file else " the given code")
            + ".",
            file=sys.stderr,
        )
        sys.exit(1)

    target_source, start_line = res
    print_highlighted(target_source, start_line)


def _parse_tree(
    tree_or_leaf: ast.AST,
    object_name: str,
    expected_parent_name: str | None = None,
    parent: ast.AST | None = None,
) -> ast.AST | None:
    """Parse the given ast for an object with name  "object_name"."""
    if hasattr(tree_or_leaf, "name") and tree_or_leaf.name == object_name:
        if not expected_parent_name:
            return tree_or_leaf

        assert parent is not None
        return (
            tree_or_leaf
            if hasattr(parent, "name") and parent.name == expected_parent_name
            else None
        )

    if not hasattr(tree_or_leaf, "body"):
        return None

    for obj in tree_or_leaf.body:
        if hasattr(obj, "body") and (
            res := _parse_tree(
                obj,
                object_name,
                parent=tree_or_leaf,
                expected_parent_name=expected_parent_name,
            )
        ):
            return res

        if not hasattr(obj, "name"):
            continue

        if obj.name != object_name:
            continue

    return None


def get_source_for_object(
    source: str,
    object_name: str,
    expected_parent: str | None = None,
) -> tuple[str, int] | None:
    """Return the source code of object by parsing the input source."""
    if res := _parse_tree(
        ast.parse(source),
        object_name,
        expected_parent_name=expected_parent,
    ):
        return ast.unparse(res), res.lineno

    return None


if __name__ == "__main__":
    cli()
