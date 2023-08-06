# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['water_cli']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'water-cli',
    'version': '0.1.6',
    'description': '',
    'long_description': '# Water\n\nLike [fire](https://github.com/google/python-fire)\n\nThis python library parses classes so that they can be executed as commands.  \nIn contrast with fire, there is no "automatic" type casting -- the type casting is 100% based on type hints.\n\n## Type casting\n\nWhen calling `execute_command` the values passed in the command get casted to the annotated types on the function\nsignature.\n\nSupported types:\n\n* int, float\n* bool: the strings `[\'true\', \'1\', \'t\', \'y\']` are considered true.\n* lists, tuples: input is split by comma (`,`) and each element is casted independently.\n\n# Examples\n\n## Type casting\n\n```python\nclass Math1:\n    def add_list(self, items: Optional[List[int]] = None):\n        if not items:\n            return 0\n        return sum(items)\n\n# `items` casted to a list of `int`\nres = execute_command(Math1, \'add_list --items 1,2,3\')\nassert res == 6\n\n# `items` casted to a list of `int`, even though there is only one entry\nres = execute_command(Math1, \'add_list --items 1\')\nassert res == 1\n```\n\n## Nested commands\n\n```python\nclass NestedObj:\n    class Inside1:\n        def fn1(self, number: int):\n            return number\n\nres = execute_command(NestedObj, \'Inside1 fn1 --number 1\')\nassert res == 1\n```\n',
    'author': 'david',
    'author_email': 'davidventura27@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DavidVentura/water',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
