from __future__ import annotations

import shutil

import pytest
from iterfzf import iterfzf  # type: ignore[import-untyped]

BAT_AVAILABLE = shutil.which("bat")
BAT_CMD = "bat --color=always --language=python"


_sentinel = object()


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


def pytest_collection_modifyitems(
    session: pytest.Session,
    config: pytest.Config,
    items: list[pytest.Function],
) -> None:
    if config.option.fzf is _sentinel:
        # not enabled
        return

    query = config.option.fzf if config.option.fzf else ""

    kwargs = {
        "multi": True,
        "prompt": "Select test(s): ",
        # see `fzf_format` for the line format
        "preview": "tail -n +{1} $(echo {2} | cut -d: -f 1)" + f"| {BAT_CMD}"
        if BAT_AVAILABLE
        else "",
        "query": query,
        "cycle": True,
    }

    def fzf_format(test: pytest.Function) -> str:
        """Format a test to be displayed with fzf.

        This is done to get a proper preview.
        """
        assert test.location[1] is not None
        line_no = test.location[1] + 1
        return f"{line_no} {test.nodeid}"

    res = iterfzf(map(fzf_format, items), **kwargs)
    if not res:
        pytest.exit("No tests selected", returncode=1)

    selected = [
        nodeid
        for line_no, nodeid in
        # the selection returned by fzf is formatted with `fzf_format`
        # re-split it to get the nodeid
        map(str.split, res)
    ]

    writer = session.config.get_terminal_writer()
    if config.option.verbose == 1:
        writer.write(f"Selected with fzf: {selected}")
    else:
        writer.write(f"Selected {len(selected)} items with fzf")

    items[:] = [test for test in items if test.nodeid in selected]
