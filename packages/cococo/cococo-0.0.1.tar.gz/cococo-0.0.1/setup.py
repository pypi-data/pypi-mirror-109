# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cococo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cococo',
    'version': '0.0.1',
    'description': '',
    'long_description': '# cococo\n\n[![PyPI](https://img.shields.io/pypi/v/tinvest)](https://pypi.org/project/tinvest/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cococo)](https://www.python.org/downloads/)\n[![GitHub last commit](https://img.shields.io/github/last-commit/daxartio/cococo)](https://github.com/daxartio/cococo)\n[![GitHub stars](https://img.shields.io/github/stars/daxartio/cococo?style=social)](https://github.com/daxartio/cococo)\n\n```\npip install cococo\n```\n',
    'author': 'Danil Akhtarov',
    'author_email': 'daxartio@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/cococo',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
