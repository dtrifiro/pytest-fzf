import shutil

from iterfzf import iterfzf  # type: ignore[import-untyped]

BAT_AVAILABLE = shutil.which("bat")
BAT_CMD = "bat --color=always --language=python"


def pytest_addoption(parser):
    group = parser.getgroup("fzf", "Test selection using fzf")
    group.addoption(
        "--fzf",
        action="store_true",
        dest="fzf_select",
        default=False,
        help="Select tests to be run using fzf.",
    )

    group.addoption(
        "--fzf-query",
        action="store",
        dest="fzf_query",
        default="",
        help="Initial fzf query.",
    )


def pytest_collection_modifyitems(
    session, config, items  # pylint: disable=unused-argument
):
    if not (config.option.fzf_select or config.option.fzf_query):
        return

    kwargs = {
        "multi": True,
        "prompt": "Select test(s)",
        "preview": "tail -n +{2} {1}" + f"| {BAT_CMD}" if BAT_AVAILABLE else "",
        "query": config.option.fzf_query,
    }

    selected = iterfzf(
        (
            f"{test.location[0]} "  # file path
            f"{int(test.location[1]) + 1} "  # line number
            f"{test.location[2]}"  # function name
            for test in items
        ),
        **kwargs,
    )

    selected_names = [test.split(" ")[2] for test in selected]

    if config.option.verbose == 1:
        print(f"\n fzf selected the following tests: {selected_names}")

    items[:] = [test for test in items if test.name in selected_names]
