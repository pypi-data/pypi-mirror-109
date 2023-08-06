# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sumadora']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['sumadora = sumadora.__main__:cli']}

setup_kwargs = {
    'name': 'sumadora',
    'version': '0.0.13',
    'description': 'Sumador básico',
    'long_description': '# Repositorio de ejemplo\n\nEste un ejemplo de repositorio\n\n## Formato de uso\n\n~~~\nsumadora "1 2 3 4 5 6"\n~~~',
    'author': 'Santiago Quiñones',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lsantiago/DemoPackage',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
