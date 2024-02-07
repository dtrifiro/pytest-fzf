from __future__ import annotations

import shutil

import pytest
from iterfzf import iterfzf  # type: ignore[import-untyped]

BAT_AVAILABLE = shutil.which("bat")
BAT_CMD = "bat --color=always --language=python"

_sentinel = object()


PYTEST_FZF_KEY = pytest.StashKey[dict[str, list[pytest.Function]]]()

FZF_KEYBINDINGS = {
    "ctrl-a": "toggle-all",
}


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("fzf", "Test selection using fzf")
    group.addoption(
        "--fzf",
        action="store",
        dest="fzf",
        default=_sentinel,
        help="Select tests to be run using fzf. Optional args provide initial query",
        nargs="?",
    )

    group.addoption(
        "--fzf-bat-preview",
        action="store_true",
        dest="use_bat",
        default=False,
        help="Use bat as fzf preview command",
    )


def pytest_collection_finish(session: pytest.Session) -> None:
    verbose = session.config.option.verbose
    if verbose < 0 or PYTEST_FZF_KEY not in session.config.stash:
        return

    deselected = session.config.stash[PYTEST_FZF_KEY]["deselected"]

    if not deselected:
        return

    writer = session.config.get_terminal_writer()
    writer.write(
        f" -> {len(deselected)} deselected by pytest-fzf{':' if verbose else ''}\n",
        bold=True,
        purple=True,
    )
    if verbose:
        for test in deselected:
            writer.write(f"  {test.nodeid}\n")


def pytest_collection_modifyitems(
    session: pytest.Session,  # noqa: ARG001
    config: pytest.Config,
    items: list[pytest.Function],
) -> None:
    if config.option.fzf is _sentinel:
        # not enabled
        return

    query = config.option.fzf if config.option.fzf else ""

    def fzf_format(test: pytest.Function) -> str:
        """Format a test to be displayed with fzf."""
        assert test.location[1] is not None
        line_no = test.location[1] + 1
        return f"{line_no:4d} │ {test.nodeid}"

    if config.option.use_bat:
        preview_command = "tail -n +{1} $(echo {3} | cut -d: -f 1)" + f"| {BAT_CMD}"
    else:
        preview_command = "pytest-fzf-preview {3}"

    kwargs = {
        "multi": True,
        "prompt": "Select test(s): ",
        "preview": preview_command,
        "query": query,
        "cycle": True,
    }

    res = iterfzf(
        map(fzf_format, items),
        __extra__=[
            "--reverse",
            "--bind={}".format(
                ",".join(
                    (f"{key}:{action}" for key, action in FZF_KEYBINDINGS.items()),
                ),
            ),
        ],
        **kwargs,
    )
    if not res:
        items[:] = []
        return

    fzf_selection = [
        nodeid
        for line_no, _, nodeid in
        # the selection returned by fzf is formatted with `fzf_format`
        # re-split it to get the nodeid
        map(str.split, res)
    ]

    selected = []
    deselected = []
    for collected in items:
        if collected.nodeid in fzf_selection:
            selected.append(collected)
            continue
        deselected.append(collected)

    config.stash[PYTEST_FZF_KEY] = {
        "deselected": deselected,
        "selected": selected,
    }

    config.hook.pytest_deselected(items=deselected)
    items[:] = selected
