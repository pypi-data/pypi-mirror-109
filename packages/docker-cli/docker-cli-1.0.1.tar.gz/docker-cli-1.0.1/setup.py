# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docker_cli']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode>=1.2.0,<2.0.0',
 'clean-text>=0.4.0,<0.5.0',
 'delegator.py>=0.1.1,<0.2.0',
 'docker-compose>=1.29.2,<2.0.0']

setup_kwargs = {
    'name': 'docker-cli',
    'version': '1.0.1',
    'description': '',
    'long_description': None,
    'author': 'Manu',
    'author_email': 'grajmanu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
