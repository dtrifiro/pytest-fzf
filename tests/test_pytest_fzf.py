def test_help_message(testdir):
    result = testdir.runpytest(
        "--help",
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "Test selection using fzf:",
            "*--fzf*Select tests to be run using fzf. Optional args provide",
            "*initial query",
        ],
    )
