# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eventual', 'eventual.abc', 'eventual.model', 'eventual.util']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.0.1,<4.0.0', 'pytz>=2021.1,<2022.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=3.10.0,<4.0.0'],
 'rmq': ['eventual-rmq>=0,<1'],
 'tortoise': ['eventual-tortoise>=0,<1']}

setup_kwargs = {
    'name': 'eventual',
    'version': '0.7.0',
    'description': '',
    'long_description': None,
    'author': 'Ivan Dmitriesvkii',
    'author_email': 'ivan.dmitrievsky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
