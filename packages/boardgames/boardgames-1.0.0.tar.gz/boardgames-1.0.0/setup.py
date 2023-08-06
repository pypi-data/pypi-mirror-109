# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['boardgames']

package_data = \
{'': ['*']}

modules = \
['py']
setup_kwargs = {
    'name': 'boardgames',
    'version': '1.0.0',
    'description': 'Board game utility functions',
    'long_description': None,
    'author': 'bijij',
    'author_email': 'josh@josh-is.gay',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
