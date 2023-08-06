# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rashsetup']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rashsetup',
    'version': '0.0.1',
    'description': 'Setup Module that can be used for both testing Rash and also Setting up Rash',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
