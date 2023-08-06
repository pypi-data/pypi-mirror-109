================================
RSC On This Day in Chemistry
================================

.. start short_desc

**Displays Royal Society of Chemistry "On This Day" facts.**

.. end short_desc

Displays Royal Society of Chemistry "On This Day" facts in your terminal.

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/rsc-on-this-day/latest?logo=read-the-docs
	:target: https://rsc-on-this-day.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/rsc-on-this-day/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/rsc-on-this-day/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/domdfcoding/rsc-on-this-day/workflows/Linux/badge.svg
	:target: https://github.com/domdfcoding/rsc-on-this-day/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/rsc-on-this-day/workflows/Windows/badge.svg
	:target: https://github.com/domdfcoding/rsc-on-this-day/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/rsc-on-this-day/workflows/macOS/badge.svg
	:target: https://github.com/domdfcoding/rsc-on-this-day/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/domdfcoding/rsc-on-this-day/workflows/Flake8/badge.svg
	:target: https://github.com/domdfcoding/rsc-on-this-day/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/domdfcoding/rsc-on-this-day/workflows/mypy/badge.svg
	:target: https://github.com/domdfcoding/rsc-on-this-day/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://requires.io/github/domdfcoding/rsc-on-this-day/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/rsc-on-this-day/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/rsc-on-this-day/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/rsc-on-this-day?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/rsc-on-this-day?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/rsc-on-this-day
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/rsc_on_this_day
	:target: https://pypi.org/project/rsc_on_this_day/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/rsc_on_this_day?logo=python&logoColor=white
	:target: https://pypi.org/project/rsc_on_this_day/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/rsc_on_this_day
	:target: https://pypi.org/project/rsc_on_this_day/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/rsc_on_this_day
	:target: https://pypi.org/project/rsc_on_this_day/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/domdfcoding/rsc-on-this-day
	:target: https://github.com/domdfcoding/rsc-on-this-day/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/rsc-on-this-day
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/rsc-on-this-day/v0.4.0
	:target: https://github.com/domdfcoding/rsc-on-this-day/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/rsc-on-this-day
	:target: https://github.com/domdfcoding/rsc-on-this-day/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2021
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/rsc_on_this_day
	:target: https://pypi.org/project/rsc_on_this_day/
	:alt: PyPI - Downloads

.. end shields


Installation
-------------

.. start installation

``rsc_on_this_day`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install rsc_on_this_day

.. end installation

Once installed, ``rsc_on_this_day`` can be run by typing:

.. parsed-literal::

        $ rsc_on_this_day

If ``rsc_on_this_day`` is not installed in a directory in ``$PATH``, you may need to add ``~/.local/bin/`` to your ``$PATH``.



Adding to ``~/.bashrc``
-----------------------

``rsc_on_this_day`` can be run every time you open a terminal by adding ``rsc_on_this_day`` to your ``~/.bashrc`` file. For example:

.. parsed-literal::

    $ echo "rsc_on_this_day" >> ~/.bashrc
