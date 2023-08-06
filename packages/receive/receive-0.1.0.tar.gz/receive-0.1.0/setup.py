# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['receive']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'receive',
    'version': '0.1.0',
    'description': 'Host a temporary HTTP server to receive a web-hook callback.',
    'long_description': None,
    'author': 'Blake Smith',
    'author_email': 'blakeinvictoria@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
