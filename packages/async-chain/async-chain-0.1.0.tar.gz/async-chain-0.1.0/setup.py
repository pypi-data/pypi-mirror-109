# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_chain', 'async_chain.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'async-chain',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Stefano Pigozzi',
    'author_email': 'me@steffo.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
