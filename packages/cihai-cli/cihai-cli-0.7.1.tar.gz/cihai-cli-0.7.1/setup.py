# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cihai_cli']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=3.12,<6', 'cihai>=0.11.0,<0.12.0', 'click>=7']

entry_points = \
{'console_scripts': ['cihai = cihai_cli.cli:cli']}

setup_kwargs = {
    'name': 'cihai-cli',
    'version': '0.7.1',
    'description': 'Command line frontend for the cihai CJK language library',
    'long_description': '*cihai-cli* - Command line interface to the `cihai`_ `CJK`_-language library\n\n|pypi| |docs| |build-status| |coverage| |license|\n\nThis project is under active development. Follow our progress and check\nback for updates!\n\nInstallation\n------------\n\n.. code-block:: sh\n\n   $ pip install --user cihai[cli]\n\nCharacter lookup\n----------------\n\nSee `CLI`_ in the documentation for full usage information.\n\n.. code-block:: sh\n\n   $ cihai info 好\n   char: 好\n   kCantonese: hou2 hou3\n   kDefinition: good, excellent, fine; well\n   kHangul: 호\n   kJapaneseOn: KOU\n   kKorean: HO\n   kMandarin: hǎo\n   kTang: \'*xɑ̀u *xɑ̌u\'\n   kTotalStrokes: \'6\'\n   ucn: U+597D\n\n   # retrieve all character information (including book indices)\n   $ cihai info 好 -a\n   char: 好\n   kCangjie: VND\n   kCantonese: hou2 hou3\n   kCihaiT: \'378.103\'\n   kDefinition: good, excellent, fine; well\n   kFenn: 552A\n   kFourCornerCode: \'4744.7\'\n   kFrequency: \'1\'\n   kGradeLevel: \'1\'\n   kHKGlyph: 0871\n   kHangul: 호\n   kHanyuPinlu: hǎo(6060) hāo(142) hào(115)\n   kHanyuPinyin: 21028.010:hǎo,hào\n   kJapaneseKun: KONOMU SUKU YOI\n   kJapaneseOn: KOU\n   kKorean: HO\n   kMandarin: hǎo\n   kPhonetic: \'481\'\n   kRSAdobe_Japan1_6: C+1975+38.3.3 C+1975+39.3.3\n   kRSKangXi: \'38.3\'\n   kTang: \'*xɑ̀u *xɑ̌u\'\n   kTotalStrokes: \'6\'\n   kVietnamese: háo\n   kXHC1983: 0445.030:hǎo 0448.030:hào\n   ucn: U+597D\n\nReverse lookup\n--------------\n\n.. code-block:: sh\n\n   $ cihai reverse library\n   char: 圕\n   kCantonese: syu1\n   kDefinition: library\n   kJapaneseOn: TOSHOKAN SHO\n   kMandarin: tú\n   kTotalStrokes: \'13\'\n   ucn: U+5715\n   --------\n   char: 嫏\n   kCantonese: long4\n   kDefinition: the place where the supreme stores his books; library\n   kJapaneseOn: ROU\n   kMandarin: láng\n   kTotalStrokes: \'11\'\n   ucn: U+5ACF\n   --------\n\nDeveloping\n----------\n`poetry`_ is a required package to develop.\n\n``git clone https://github.com/cihai/cihai-cli.git``\n\n``cd cihai-cli``\n\n``poetry install -E "docs test coverage lint format"``\n\nMakefile commands prefixed with ``watch_`` will watch files and rerun.\n\nTests\n"""""\n``poetry run py.test``\n\nHelpers: ``make test``\nRerun tests on file change: ``make watch_test`` (requires `entr(1)`_)\n\nDocumentation\n"""""""""""""\nDefault preview server: http://localhost:8037\n\n``cd docs/`` and ``make html`` to build. ``make serve`` to start http server.\n\nHelpers:\n``make build_docs``, ``make serve_docs``\n\nRebuild docs on file change: ``make watch_docs`` (requires `entr(1)`_)\n\nRebuild docs and run server via one terminal: ``make dev_docs``  (requires above, and a \n``make(1)`` with ``-J`` support, e.g. GNU Make)\n\nFormatting / Linting\n""""""""""""""""""""\nThe project uses `black`_ and `isort`_ (one after the other) and runs `flake8`_ via \nCI. See the configuration in `pyproject.toml` and `setup.cfg`:\n\n``make black isort``: Run ``black`` first, then ``isort`` to handle import nuances\n``make flake8``, to watch (requires ``entr(1)``): ``make watch_flake8`` \n\nReleasing\n"""""""""\n\nAs of 0.6, `poetry`_ handles virtualenv creation, package requirements, versioning,\nbuilding, and publishing. Therefore there is no setup.py or requirements files.\n\nUpdate `__version__` in `__about__.py` and `pyproject.toml`::\n\n\tgit commit -m \'build(cihai-cli): Tag v0.1.1\'\n\tgit tag v0.1.1\n\tgit push\n\tgit push --tags\n\tpoetry build\n\tpoetry deploy\n\n.. _poetry: https://python-poetry.org/\n.. _entr(1): http://eradman.com/entrproject/\n.. _black: https://github.com/psf/black\n.. _isort: https://pypi.org/project/isort/\n.. _flake8: https://flake8.pycqa.org/\n\nQuick links\n-----------\n- `Usage`_\n- Python `API`_\n- `2017 roadmap <https://cihai.git-pull.com/design-and-planning/2017/spec.html>`_\n\n.. _API: https://cihai-cli.git-pull.com/api.html\n.. _Usage: https://cihai-cli.git-pull.com/usage.html\n.. _CLI: https://cihai-cli.git-pull.com/cli.html\n\n- Python support: >= 3.6, pypy\n- Source: https://github.com/cihai/cihai-cli\n- Docs: https://cihai-cli.git-pull.com\n- Changelog: https://cihai-cli.git-pull.com/history.html\n- API: https://cihai-cli.git-pull.com/api.html\n- Issues: https://github.com/cihai/cihai-cli/issues\n- Test coverage   https://codecov.io/gh/cihai/cihai-cli\n- pypi: https://pypi.python.org/pypi/cihai-cli\n- OpenHub: https://www.openhub.net/p/cihai-cli\n- License: MIT\n\n.. |pypi| image:: https://img.shields.io/pypi/v/cihai_cli.svg\n    :alt: Python Package\n    :target: http://badge.fury.io/py/cihai_cli\n\n.. |docs| image:: https://github.com/cihai/cihai-cli/workflows/Publish%20Docs/badge.svg\n   :alt: Docs\n   :target: https://github.com/cihai/cihai-cli/actions?query=workflow%3A"Publish+Docs"\n\n.. |build-status| image:: https://github.com/cihai/cihai-cli/workflows/tests/badge.svg\n   :alt: Build Status\n   :target: https://github.com/cihai/cihai-cli/actions?query=workflow%3A"tests"\n\n.. |coverage| image:: https://codecov.io/gh/cihai/cihai-cli/branch/master/graph/badge.svg\n    :alt: Code Coverage\n    :target: https://codecov.io/gh/cihai/cihai-cli\n\n.. |license| image:: https://img.shields.io/github/license/cihai/cihai-cli.svg\n    :alt: License \n\n.. _cihai: https://cihai.git-pull.com\n.. _CJK: https://cihai.git-pull.com/glossary.html#term-cjk\n.. _UNIHAN: http://unicode.org/charts/unihan.html\n',
    'author': 'Tony Narlock',
    'author_email': 'tony@git-pull.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://cihai-cli.git-pull.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
