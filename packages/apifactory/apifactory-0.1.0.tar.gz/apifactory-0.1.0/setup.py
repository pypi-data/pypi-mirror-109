# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apifactory']

package_data = \
{'': ['*']}

install_requires = \
['bcrypt>=3.2.0,<4.0.0',
 'fastapi>=0.65.1,<0.66.0',
 'passlib>=1.7.4,<2.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pymssql>=2.2.1,<3.0.0',
 'python-jose>=3.2.0,<4.0.0',
 'python-multipart>=0.0.5,<0.0.6',
 'sqlalchemy>=1.4.7,<2.0.0',
 'uvicorn>=0.13.4,<0.14.0']

setup_kwargs = {
    'name': 'apifactory',
    'version': '0.1.0',
    'description': 'package for automatically creating an api on an existing database',
    'long_description': None,
    'author': 'Sebastiaan Broekema',
    'author_email': 'sebastiaanbroekema@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
