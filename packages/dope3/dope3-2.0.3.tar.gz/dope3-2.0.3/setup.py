# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dope3']

package_data = \
{'': ['*']}

install_requires = \
['bchlib>=0.14.0,<0.15.0', 'dill>=0.3.3,<0.4.0', 'pycryptodome>=3.9,<4.0']

setup_kwargs = {
    'name': 'dope3',
    'version': '2.0.3',
    'description': 'Python3 Implementation of DOPE Encryption',
    'long_description': None,
    'author': 'Anubhav Mattoo',
    'author_email': 'anubhavmattoo@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
