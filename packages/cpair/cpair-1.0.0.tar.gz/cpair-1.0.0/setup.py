# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cpair']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cpair',
    'version': '1.0.0',
    'description': 'Find the minimum distance between a set of points in linear time.',
    'long_description': None,
    'author': 'Kian Cross',
    'author_email': 'kian@kiancross.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
