# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cihai', 'cihai.data', 'cihai.data.decomp', 'cihai.data.unihan']

package_data = \
{'': ['*']}

install_requires = \
['appdirs',
 'click>=7',
 'kaptan',
 'sqlalchemy<1.4',
 'unihan-etl>=0.12.0,<0.13.0']

extras_require = \
{'cli': ['cihai-cli']}

setup_kwargs = {
    'name': 'cihai',
    'version': '0.11.1',
    'description': 'Library for CJK (chinese, japanese, korean) language data.',
    'long_description': '*cihai* - Python library for `CJK`_ (chinese, japanese, korean) data\n\n|pypi| |docs| |build-status| |coverage| |license|\n\nThis project is under active development. Follow our progress and check\nback for updates!\n\nUsage\n-----\n\nAPI / Library (this repository)\n"""""""""""""""""""""""""""""""\n\n.. code-block:: sh\n\n   $ pip install --user cihai\n\n.. code-block:: python\n\n   from cihai.core import Cihai\n\n   c = Cihai()\n\n   if not c.unihan.is_bootstrapped:  # download and install Unihan to db\n       c.unihan.bootstrap(unihan_options)\n\n   query = c.unihan.lookup_char(\'好\')\n   glyph = query.first()\n   print("lookup for 好: %s" % glyph.kDefinition)\n   # lookup for 好: good, excellent, fine; well\n\n   query = c.unihan.reverse_char(\'good\')\n   print(\'matches for "good": %s \' % \', \'.join([glph.char for glph in query]))\n   # matches for "good": 㑘, 㑤, 㓛, 㘬, 㙉, 㚃, 㚒, 㚥, 㛦, 㜴, 㜺, 㝖, 㤛, 㦝, ...\n\nSee `API`_ documentation and `/examples\n<https://github.com/cihai/cihai/tree/master/examples>`_.\n\nCLI (`cihai-cli`_)\n""""""""""""""""""\n\n.. code-block:: sh\n\n   $ pip install --user cihai[cli]\n\n.. code-block:: sh\n\n   # character lookup\n   $ cihai info 好\n   char: 好\n   kCantonese: hou2 hou3\n   kDefinition: good, excellent, fine; well\n   kHangul: 호\n   kJapaneseOn: KOU\n   kKorean: HO\n   kMandarin: hǎo\n   kTang: \'*xɑ̀u *xɑ̌u\'\n   kTotalStrokes: \'6\'\n   kVietnamese: háo\n   ucn: U+597D\n\n   # reverse lookup\n   $ cihai reverse library\n   char: 圕\n   kCangjie: WLGA\n   kCantonese: syu1\n   kCihaiT: \'308.302\'\n   kDefinition: library\n   kMandarin: tú\n   kTotalStrokes: \'13\'\n   ucn: U+5715\n   --------\n\nUNIHAN data\n"""""""""""\nAll datasets that cihai uses have stand-alone tools to export their data.\nNo library required.\n\n- `unihan-etl <https://unihan-etl.git-pull.com>`_ - `UNIHAN`_ data\n  exports for csv, yaml and json.\n\nDeveloping\n----------\n`poetry`_ is a required package to develop.\n\n``git clone https://github.com/cihai/cihai.git``\n\n``cd cihai``\n\n``poetry install -E "docs test coverage lint format"``\n\nMakefile commands prefixed with ``watch_`` will watch files and rerun.\n\nTests\n"""""\n``poetry run py.test``\n\nHelpers: ``make test``\nRerun tests on file change: ``make watch_test`` (requires `entr(1)`_)\n\nDocumentation\n"""""""""""""\nDefault preview server: http://localhost:8035\n\n``cd docs/`` and ``make html`` to build. ``make serve`` to start http server.\n\nHelpers:\n``make build_docs``, ``make serve_docs``\n\nRebuild docs on file change: ``make watch_docs`` (requires `entr(1)`_)\n\nRebuild docs and run server via one terminal: ``make dev_docs``  (requires above, and a \n``make(1)`` with ``-J`` support, e.g. GNU Make)\n\nFormatting / Linting\n""""""""""""""""""""\nThe project uses `black`_ and `isort`_ (one after the other) and runs `flake8`_ via \nCI. See the configuration in `pyproject.toml` and `setup.cfg`:\n\n``make black isort``: Run ``black`` first, then ``isort`` to handle import nuances\n``make flake8``, to watch (requires ``entr(1)``): ``make watch_flake8`` \n\nReleasing\n"""""""""\nAs of 0.10, `poetry`_ handles virtualenv creation, package requirements, versioning,\nbuilding, and publishing. Therefore there is no setup.py or requirements files.\n\nUpdate `__version__` in `__about__.py` and `pyproject.toml`::\n\n\tgit commit -m \'build(cihai): Tag v0.1.1\'\n\tgit tag v0.1.1\n\tgit push\n\tgit push --tags\n\tpoetry build\n\tpoetry deploy\n\n.. _poetry: https://python-poetry.org/\n.. _entr(1): http://eradman.com/entrproject/\n.. _black: https://github.com/psf/black\n.. _isort: https://pypi.org/project/isort/\n.. _flake8: https://flake8.pycqa.org/\n\nQuick links\n-----------\n- `Usage`_\n- `Datasets`_ a full list of current and future data sets\n- Python `API`_\n- `Roadmap <https://cihai.git-pull.com/design-and-planning/>`_\n\n.. _API: https://cihai.git-pull.com/api.html\n.. _Datasets: https://cihai.git-pull.com/datasets.html\n.. _Usage: https://cihai.git-pull.com/usage.html\n\n- Python support: Python 2.7, >= 3.5, pypy\n- Source: https://github.com/cihai/cihai\n- Docs: https://cihai.git-pull.com\n- Changelog: https://cihai.git-pull.com/history.html\n- API: https://cihai.git-pull.com/api.html\n- Issues: https://github.com/cihai/cihai/issues\n- Test coverage: https://codecov.io/gh/cihai/cihai\n- pypi: https://pypi.python.org/pypi/cihai\n- OpenHub: https://www.openhub.net/p/cihai\n- License: MIT\n\n.. |pypi| image:: https://img.shields.io/pypi/v/cihai.svg\n    :alt: Python Package\n    :target: http://badge.fury.io/py/cihai\n\n.. |docs| image:: https://github.com/cihai/cihai/workflows/Publish%20Docs/badge.svg\n   :alt: Docs\n   :target: https://github.com/cihai/cihai/actions?query=workflow%3A"Publish+Docs"\n\n.. |build-status| image:: https://github.com/cihai/cihai/workflows/test/badge.svg\n   :alt: Build Status\n   :target: https://github.com/cihai/cihai/actions?query=workflow%3A"test"\n\n.. |coverage| image:: https://codecov.io/gh/cihai/cihai/branch/master/graph/badge.svg\n    :alt: Code Coverage\n    :target: https://codecov.io/gh/cihai/cihai\n\n.. |license| image:: https://img.shields.io/github/license/cihai/cihai.svg\n    :alt: License \n\n.. _CJK: https://cihai.git-pull.com/glossary.html#term-cjk\n.. _UNIHAN: http://unicode.org/charts/unihan.html\n.. _variants: http://www.unicode.org/reports/tr38/tr38-21.html#N10211\n.. _cihai.conversion: http://cihai.git-pull.com/api.html#conversion\n.. _cihai-cli: https://cihai-cli.git-pull.com\n',
    'author': 'Tony Narlock',
    'author_email': 'tony@git-pull.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://cihai.git-pull.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
