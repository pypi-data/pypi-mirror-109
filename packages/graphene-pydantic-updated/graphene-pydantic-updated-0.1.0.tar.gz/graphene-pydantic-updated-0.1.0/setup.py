# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphene_pydantic_updated']

package_data = \
{'': ['*']}

install_requires = \
['graphene>=3.0b5', 'pydantic>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'graphene-pydantic-updated',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jeremy Berman',
    'author_email': 'jerber@sas.upenn.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
