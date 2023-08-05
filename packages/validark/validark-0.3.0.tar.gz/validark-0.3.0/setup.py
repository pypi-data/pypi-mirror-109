# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['validark']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'validark',
    'version': '0.3.0',
    'description': 'Simple Data Validation Library',
    'long_description': None,
    'author': 'Knowark',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
