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
    'version': '1.0.2',
    'description': 'A straight forward tool to get information from docker command line and try to parse into json format as far as possible.',
    'long_description': '# Docker-cli\n \nA straight forward tool to get information from docker command line and try to parse into json format as far as possible.\n\n## Why not docker api?\n- The api schema might change and response data might change so often.\n- Docker-cli uses docker cli to get response and try to format them into json format\n\n## Installation\n`pip install docker-cli`\n\n## Main methods\n- `is_docker_set()` to verify docker installation and availability\n```bash\n docker_cli.is_docker_set() \n```\n- To run docker commands\n```bash\n Request: docker_cli.docker("ps") \n \n Response Structure:\n DockerResponse(command=\'docker ps\', status=\'SUCCESS\', type=\'JSON\', data=[<JSON Data>])\n\n```\n- To run docker commands\n```bash\n Request: docker_cli.docker_compose("up -d") \n \n Response Structure:\n Similar as that of docker commands\n```',
    'author': 'Manu',
    'author_email': 'grajmanu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/manugraj/docker-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
