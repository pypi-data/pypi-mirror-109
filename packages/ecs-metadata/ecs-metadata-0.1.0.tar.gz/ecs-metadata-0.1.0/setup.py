# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecs_metadata']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'ecs-metadata',
    'version': '0.1.0',
    'description': 'Get the meta data of the current ECS container, or empty variables if outside of ECS.',
    'long_description': None,
    'author': 'Paris Kasidiaris',
    'author_email': 'paris@kasidiaris.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
