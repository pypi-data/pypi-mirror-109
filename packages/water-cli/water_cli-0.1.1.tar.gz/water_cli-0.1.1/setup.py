# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['water_cli']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'water-cli',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'david',
    'author_email': 'davidventura27@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
