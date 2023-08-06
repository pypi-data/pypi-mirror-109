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
    'version': '0.1.1',
    'description': 'Python command line application to backup IDE / code editor settings. ',
    'long_description': "# snit\n\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nPython command line application to backup IDE / code editor settings. \n**Currently only VSCode is supported**.\n\nMotivation: I have most of my projects in Github, but don't want to put editor settings there.  This lets me save the important information in *launch.json*, *settings.json*, to some central location. \n\n\n## Project Features\n\n* Simply copies files to given destination \n* files are numgered sequentially, like old-school [VMS](https://en.wikipedia.org/wiki/Versioning_file_system#Files-11_(RSX-11_and_OpenVMS))\n* files are compared so only changed files are backed up.\n* numbering preserves the extension so the OS still recognizes the file type.\n\n\n## Alternatives\n\nVSCode offers settings sync, but not for workspaces, only for user settings.\n\nGit, Hg, etc. seem too heavy.\n\n## Installation\n\n    $ pip install snit\n\n## Usage\n    $ snit [OPTIONS] COMMAND\n\n    Options:\n       -a, --archive PATH    Specify the directory for the archive.  Can be set with\n                             the SNIT_DIR environment variable.  [required]\n       --help                Show this message and exit.\n\n    Commands:\n        backup  Backup editor settings.  \n        list    List any found backups.  \n\n## Example:\n(Windows, with `SNIT_DIR` set)\n\n    D:\\Code\\MyBigProject>snit backup\n\nCopies workspace settings to `$SNIT_DIR\\D__Code_MyBigProject\\vscode`\n\n## ToDo\nVerify Unix compatibility.",
    'author': 'Norman Lorrain',
    'author_email': 'normanlorrain@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/normanlorrain/snit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
