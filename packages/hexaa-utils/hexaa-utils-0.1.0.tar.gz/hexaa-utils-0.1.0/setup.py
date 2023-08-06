# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hexaa_utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hexaa-utils',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Song',
    'author_email': 'songhe@hexaa.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
