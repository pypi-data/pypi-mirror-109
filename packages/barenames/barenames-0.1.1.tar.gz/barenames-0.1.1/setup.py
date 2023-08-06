# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['barenames', 'barenames.lib']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['barenames = barenames.__main__:main']}

setup_kwargs = {
    'name': 'barenames',
    'version': '0.1.1',
    'description': 'Batch file rename tool',
    'long_description': '# Barenames\n\nCommandline tool for batch renaming files using regular expressions.\n\n## Usage\n\n```\nUsage: barenames [OPTIONS] PATTERN REPLACEMENT\n\n  Batch file rename tool with regex substitution.\n\n  Example:\n\n      barenames "myfile-(\\d+)" "yourfile-\\g<1>"\n\nOptions:\n  --dir PATH                Directory to perform actions in (default: current\n                            working directory)\n  --preview / --no-preview  Show preview of renames with confirmation prompt.\n  -r, --recursive           Search files to rename recursively\n  --help                    Show this message and exit\n```\n\nBarenames uses regex to change file names, which is very powerful tool.\nBut power comes with responsibility, **it is adviced to use `--preview` option to\nview what program is gonna do, before it does it, cause with regex you never truly know....**\n\n### Change file extension:\n\nThis example changes extension of all `.md` files in\ncurrent working directory to `.rst`\n\n```sh\nbarenames --preview "(?P<filename>.+)\\.md" "\\g<filename>.rst"\n```\n\nIf your files are not in current working directory just pass\n`--dir` option to override dir.\n\n```sh\nbarenames --dir ~/my-notes/ --preview "(?P<filename>.+)\\.md" "\\g<filename>.rst"\n```\n\nIf you wish to rename files in subdirectories too, use `--recursive` or `-r` for short.\n\n```sh\nbarenames --recursive --preview "(?P<filename>.+)\\.md" "\\g<filename>.rst"\n```\n\nUse this option with caution though.\n',
    'author': 'Crystal Melting Dot',
    'author_email': 'stresspassing@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cmd410/barenames',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
