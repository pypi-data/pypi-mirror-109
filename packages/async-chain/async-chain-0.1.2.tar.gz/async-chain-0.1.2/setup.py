# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_chain', 'async_chain.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'async-chain',
    'version': '0.1.2',
    'description': 'A coroutine builder',
    'long_description': '# `async-chain`\n\nA coroutine builder\n\n\n## What?\n\nHave you ever felt that the `await` syntax in Python was a bit clunky when chaining multiple methods together?\n\n```python\nasync def on_message(event):\n    message = await event.get_message()\n    author = await message.get_author()\n    await author.send_message("Hello world!")\n```\n\nOr even worse:\n\n```python\nasync def on_message(event):\n    (await (await (await event.get_message()).get_author()).send_message("Hello world!"))\n```\n\n`async-chain` is here to solve your problem!\n\n```python\nasync def on_message(event):\n    await event.get_message().get_author().send_message("Hello world!")\n```\n\n\n## How?\n\nFirst, install `async_chain` with your favorite package manager:\n\n```console\n$ pip install async_chain\n```\n```console\n$ pipenv install async_chain\n```\n```console\n$ poetry add async_chain\n```\n\nThen, add the `@async_chain.method` decorator to any async method you wish to make chainable, and the problem will be \nmagically solved!\n\n```python\nimport async_chain\n\nclass MyEvent:\n    @async_chain.method\n    async def get_message(self):\n        ...\n```\n',
    'author': 'Stefano Pigozzi',
    'author_email': 'me@steffo.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Steffo99/async-chain',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
