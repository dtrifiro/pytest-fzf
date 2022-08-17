==========
pytest-fzf
==========

.. image:: https://img.shields.io/pypi/v/pytest-fzf.svg
    :target: https://pypi.org/project/pytest-fzf
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-fzf.svg
    :target: https://pypi.org/project/pytest-fzf
    :alt: Python versions

.. |Tests| image:: https://github.com/dtrifiro/pytest-fzf/workflows/Tests/badge.svg
   :target: https://github.com/dtrifiro/pytest-fzf/actions?workflow=Tests
   :alt: Tests

fzf-based test selection with pytest

----

Features
--------

* Select tests to be run with pytest using fzf


Requirements
------------

* `fzf` (https://github.com/junegunn/fzf)
* (Optional, for colored preview of test functions) `bat` (https://github.com/sharkdp/bat)


Installation
------------

You can install "pytest-fzf" via `pip`_ from `PyPI`_::

    $ pip install pytest-fzf


Usage
-----

.. code:: console

   $ pytest --fzf

Select multiple tests using `tab`, deselect previously selected tests using `shift+tab`

In order to start fzf with a given query:

.. code:: console

   $ pytest --fzf --fzf-query=<query>


Contributing
------------
Contributions are very welcome. Tests can be run with `nox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `GNU GPL v3.0`_ license, "pytest-fzf" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`file an issue`: https://github.com/dtrifiro/pytest-fzf/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`nox`: https://github.com/wntrblm/nox
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
