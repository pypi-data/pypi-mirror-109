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
    'version': '0.7.0',
    'description': 'Command line frontend for the cihai CJK language library',
    'long_description': None,
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
