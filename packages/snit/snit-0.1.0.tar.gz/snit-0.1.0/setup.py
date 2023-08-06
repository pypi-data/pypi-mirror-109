# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snit']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['snit = snit.cli:cli']}

setup_kwargs = {
    'name': 'snit',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Norman Lorrain',
    'author_email': 'normanlorrain@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
