# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swag']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'swag',
    'version': '1.6.0',
    'description': 'Swag up your shell output with escape code magic!',
    'long_description': None,
    'author': '4thel00z',
    'author_email': '4thel00z@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
