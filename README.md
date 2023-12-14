# pytest-fzf

[![PyPI version](https://img.shields.io/pypi/v/pytest-fzf.svg)](https://pypi.org/project/pytest-fzf)
[![Python versions](https://img.shields.io/pypi/pyversions/pytest-fzf.svg)](https://pypi.org/project/pytest-fzf)
[![Tests](https://github.com/dtrifiro/pytest-fzf/actions/workflows/tests.yml/badge.svg)](https://github.com/dtrifiro/pytest-fzf/actions/workflows/tests.yml)

fzf-based test selection with `pytest`

[![demo](https://github.com/dtrifiro/pytest-fzf/assets/36171005/29f7a610-2f15-402f-a24f-af8bf7e0e71d)](https://asciinema.org/a/iAr18ilruuPM7pZ1EAfXkxfEf)

---

## Features

- Select tests to be run with pytest using fzf

## Requirements

- [fzf](https://github.com/junegunn/fzf)
- (Optional, for colored preview of test functions) `bat`[sharkdp/bat](https://github.com/sharkdp/bat)

## Installation

You can install `pytest-fzf` via [pip](https://pypi.org/project/pip/)
from [PyPI](https://pypi.org/project):

```bash
pip install pytest-fzf
```

## Usage

```bash
pytest --fzf [query]
```

### Keybindings

The following keybindings can be used in the fzf selection menu

- Tab: selected/deselect tests
- Shift+Tab: selected/deselect tests (move up)
- Ctrl+a: select/deselect all tests

## Contributing

Contributions are very welcome. Tests can be run with
[nox](https://github.com/wntrblm/nox), please ensure the coverage at
least stays the same before you submit a pull request.

## License

Distributed under the terms of the [GNU GPL
v3.0](http://www.gnu.org/licenses/gpl-3.0.txt) license, `pytest-fzf`
is free and open source software

## Issues

If you encounter any problems, please [file an
issue](https://github.com/dtrifiro/pytest-fzf/issues) along with a
detailed description.
