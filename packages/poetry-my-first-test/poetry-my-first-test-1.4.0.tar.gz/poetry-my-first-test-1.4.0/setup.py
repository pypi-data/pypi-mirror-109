# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_my_first_test', 'poetry_my_first_test.views']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['my-cmd = poetry_my_first_test.cli:cli']}

setup_kwargs = {
    'name': 'poetry-my-first-test',
    'version': '1.4.0',
    'description': '',
    'long_description': None,
    'author': 'puntonim',
    'author_email': 'puntonim@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
