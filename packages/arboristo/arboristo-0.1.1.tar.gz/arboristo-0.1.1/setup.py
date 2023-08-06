# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arboristo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'arboristo',
    'version': '0.1.1',
    'description': 'A light-weight package to lazily traverse a deeply nested dictionary',
    'long_description': '# arboristo\n[![Build Status](https://github.com/AlanAutomated/arboristo/workflows/CI/badge.svg)](https://github.com/AlanAutomated/arboristo/actions)\n[![codecov](https://codecov.io/gh/AlanAutomated/arboristo/branch/master/graph/badge.svg?token=IYHABMICSN)](https://codecov.io/gh/AlanAutomated/arboristo) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/7c212a68576d4536a08a4a448361b497)](https://www.codacy.com/gh/AlanAutomated/arboristo/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=AlanAutomated/arboristo&amp;utm_campaign=Badge_Grade) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai)\n\nA light-weight package to lazily traverse a deeply nested dictionary.\n\n![demo](https://raw.githubusercontent.com/AlanAutomated/arboristo/master/demo.gif)\n',
    'author': 'Alan Haynes',
    'author_email': 'alan@nre.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AlanAutomated/arboristo',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
