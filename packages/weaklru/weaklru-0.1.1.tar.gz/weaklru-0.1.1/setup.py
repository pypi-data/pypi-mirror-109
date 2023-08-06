# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weaklru']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'weaklru',
    'version': '0.1.1',
    'description': 'Combination of weakref cache and LRU cache.',
    'long_description': '# weaklru\n\nSimple combination of a weakref cache and a lru cache.\n\n```\n\nclass Obj:\n  pass\n\n\nl = WeakLRU(max_size=2)\n\nl.set("a", Obj())\nl.set("b", Obj())\nl.set("c", Obj())\nl.get(a)        # none\nl.get(b)        # obj\nl.get(c)        # obj\n```\n\n\nYou can add objects to the cache, and they will never expire as long as they are being used.\n\nAlso, a maximum number of objects will be stored in the LRU portion of the cache.\n',
    'author': 'Erik Aronesty',
    'author_email': 'erik@q32.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AtakamaLLC/weaklru',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
