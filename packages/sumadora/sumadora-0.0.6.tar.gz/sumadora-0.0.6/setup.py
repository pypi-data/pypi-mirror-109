# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sumadora']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

setup_kwargs = {
    'name': 'sumadora',
    'version': '0.0.6',
    'description': 'Sumador básico',
    'long_description': None,
    'author': 'Santiago Quiñones',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
