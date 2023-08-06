# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['osin']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'osin',
    'version': '0.1.0',
    'description': 'Rethink Experimenting',
    'long_description': None,
    'author': 'Binh Vu',
    'author_email': 'binh@toan2.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
