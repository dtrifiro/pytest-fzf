---
title: pytest-fzf
---

[![PyPI version](https://img.shields.io/pypi/v/pytest-fzf.svg)](https://pypi.org/project/pytest-fzf)
[![Python versions](https://img.shields.io/pypi/pyversions/pytest-fzf.svg)](https://pypi.org/project/pytest-fzf)
[![Tests](https://github.com/dtrifiro/pytest-fzf/actions/workflows/tests.yml/badge.svg)](https://github.com/dtrifiro/pytest-fzf/actions/workflows/tests.yml)

fzf-based test selection with `pytest`

[![demo](https://asciinema.org/a/iAr18ilruuPM7pZ1EAfXkxfEf.svg)](https://asciinema.org/a/iAr18ilruuPM7pZ1EAfXkxfEf)

---

# Features

- Select tests to be run with pytest using fzf

# Requirements

- [fzf](https://github.com/junegunn/fzf)
- (Optional, for colored preview of test functions) [`bat`](https://github.com/sharkdp/bat)
  (<https://github.com/sharkdp/bat>)

# Installation

You can install `pytest-fzf` via [pip](https://pypi.org/project/pip/)
from [PyPI](https://pypi.org/project):

```bash
pip install pytest-fzf
```

# Usage

```bash
pytest --fzf [query]
```

Select multiple tests using tab (shift+tab selects and moves up), deselect previously
selected tests using using tab again.

Optionally, the initial query can be specified from the command line:

```bash
pytest --fzf query
```

# Contributing

Contributions are very welcome. Tests can be run with
[nox](https://github.com/wntrblm/nox), please ensure the coverage at
least stays the same before you submit a pull request.

# License

Distributed under the terms of the [GNU GPL
v3.0](http://www.gnu.org/licenses/gpl-3.0.txt) license, `pytest-fzf`
is free and open source software

# Issues

If you encounter any problems, please [file an
issue](https://github.com/dtrifiro/pytest-fzf/issues) along with a
detailed description.
