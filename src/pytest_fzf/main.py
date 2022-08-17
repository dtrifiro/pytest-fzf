# -*- coding: utf-8 -*-

import pytest


def pytest_addoption(parser):
    group = parser.getgroup("fzf")
    group.addoption(
        "--fzf",
        action="store",
        dest="fzf_select",
        default=False,
        help="Filter tests using fzf",
    )

    parser.addini("HELLO", "Dummy pytest.ini setting")


def pytest_collection_modifyitems(session, config, items):
    raise NotImplementedError


@pytest.fixture
def bar(request):
    return request.config.option.dest_foo
