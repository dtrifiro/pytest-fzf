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
    session: pytest.Session,  # noqa: ARG001
    config: pytest.Config,
    items: dict,
) -> None:
    if config.option.fzf is _sentinel:
        # not enabled
        return

    query = config.option.fzf if config.option.fzf else ""

    kwargs = {
        "multi": True,
        "prompt": "Select test(s): ",
        "preview": "tail -n +{2} {1}" + f"| {BAT_CMD}" if BAT_AVAILABLE else "",
        "query": query,
        "cycle": True,
    }

    try:
        selected = iterfzf(
            (
                f"{test.location[0]} "  # file path
                f"{int(test.location[1]) + 1} "  # line number
                f"{test.location[2]}"  # function name
                for test in items
            ),
            **kwargs,
        )
    except KeyboardInterrupt:
        pytest.exit("No tests selected", returncode=0)

    if not selected:
        pytest.exit("No tests selected", returncode=0)

    selected_names = [test.split(" ")[2] for test in selected]

    if config.option.verbose == 1:
        print(f"\n fzf selected the following tests: {selected_names}")  # noqa: T201

    items[:] = [test for test in items if test.name in selected_names]
