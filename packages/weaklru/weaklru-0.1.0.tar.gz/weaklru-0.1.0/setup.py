# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weaklru']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'weaklru',
    'version': '0.1.0',
    'description': 'Combination of weakref cache and LRU cache.',
    'long_description': None,
    'author': 'Erik Aronesty',
    'author_email': 'erik@q32.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
