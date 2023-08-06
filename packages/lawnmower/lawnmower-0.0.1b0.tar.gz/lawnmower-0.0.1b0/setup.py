# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lawnmower']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['lawnmower = lawnmower:main']}

setup_kwargs = {
    'name': 'lawnmower',
    'version': '0.0.1b0',
    'description': 'LAWNMOWER - Simple Python task runner',
    'long_description': None,
    'author': 'arnu515',
    'author_email': 'arnu515@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
