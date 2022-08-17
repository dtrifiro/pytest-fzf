from iterfzf import iterfzf


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
    if not config.option.fzf_select:
        return

    kwargs = {
        "multi": True,
        "prompt": "Select test(s)",
        "preview": None,  # TODO: add preview to show test code
        "query": config.option.fzf_query,
    }
    selected_names = iterfzf((test.name for test in items), *kwargs)

    if config.option.verbose == 1:
        print(f"\n fzf selected the following tests: {selected_names}")

    items[:] = [test for test in items if test.name in selected_names]
