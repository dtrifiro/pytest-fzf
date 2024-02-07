from contextlib import suppress

import pytest

from pytest_fzf.previewer import _get_formatter, get_source_for_object, parse_nodespec


@pytest.mark.parametrize(
    ("nodespec", "expected"),
    [
        (
            "path/to/test_module.py::className::test_name",
            ("path/to/test_module.py", "className", "test_name", []),
        ),
        (
            "path/to/test_module.py::test_name",
            ("path/to/test_module.py", None, "test_name", []),
        ),
        (
            "test_module.py::test_name",
            ("test_module.py", None, "test_name", []),
        ),
        (
            "test_module.py::test_name[param]",
            ("test_module.py", None, "test_name", ["param"]),
        ),
        (
            "test_module.py::test_name[param1,param2]",
            ("test_module.py", None, "test_name", ["param1", "param2"]),
        ),
    ],
)
def test_parse_nodespec(nodespec, expected):
    parsed = parse_nodespec(nodespec)
    # parsed ~= file, name, parent, params
    assert parsed == expected


@pytest.fixture()
def _clean_theme_env_vars(monkeypatch):
    """Remove environment vars which modify theme settings."""
    for env_var in ("BAT_THEME", "PYTEST_FZF_THEME"):
        with suppress(KeyError):
            monkeypatch.delenv(env_var)


@pytest.mark.parametrize(
    ("env", "expected"),
    [
        (("PYTEST_FZF_THEME", "gruvbox-dark"), "GruvboxDarkStyle"),
        (("PYTEST_FZF_THEME", "gruvbox-light"), "GruvboxLightStyle"),
        (("BAT_THEME", "gruvbox-dark"), "GruvboxDarkStyle"),
        (("BAT_THEME", "gruvbox-light"), "GruvboxLightStyle"),
    ],
)
@pytest.mark.usefixtures("_clean_theme_env_vars")
def test_previewer_theme(monkeypatch, env, expected):
    """Test theme overrides using env vars."""
    monkeypatch.setenv(*env)
    formatter = _get_formatter()
    assert formatter.style.__name__ == expected


@pytest.mark.usefixtures("_clean_theme_env_vars")
def test_previewer_theme_default():
    """Test default highlight theme."""
    formatter = _get_formatter()
    assert formatter.style.__name__ == "DefaultStyle"


@pytest.mark.usefixtures("_clean_theme_env_vars")
def test_previewer_theme_invalid(monkeypatch, caplog):
    """Test default highlight theme."""
    monkeypatch.setenv("PYTEST_FZF_THEME", "foo")

    with pytest.warns() as warning:
        formatter = _get_formatter()
        assert (
            warning.list[0].message.args[0]
            == 'Could not find pygments style: "foo", falling back to default.'
        )

    assert formatter.style.__name__ == "DefaultStyle"


def test_get_source_for_object():
    code = """var = 1

def function(x):
    print(f"hello {x}")

for el in range(10):
    function(el)
"""

    source, line_no = get_source_for_object(code, "function")
    assert line_no
    assert source == "def function(x):\n    print(f'hello {x}')"


def test_get_source_for_object_class():
    code = """var = 1

class AnotherClass:
    def function(self, x):
        print(f"😡")

class Class:
    def function(self, x):
        print(f"hello {x}")
"""

    source, line_no = get_source_for_object(code, "function", expected_parent="Class")
    assert line_no
    assert source == "def function(self, x):\n    print(f'hello {x}')"
