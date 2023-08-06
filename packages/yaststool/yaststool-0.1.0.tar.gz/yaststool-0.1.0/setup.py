# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yaststool']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.96,<2.0.0', 'click>=8.0.1,<9.0.0', 'dacite>=1.6.0,<2.0.0']

entry_points = \
{'console_scripts': ['yaststool = yaststool.main:cli']}

setup_kwargs = {
    'name': 'yaststool',
    'version': '0.1.0',
    'description': 'A tool to assume AWS Roles and set environment variables accordingly',
    'long_description': None,
    'author': 'William Trépanier',
    'author_email': 'wtrepanier@coveo.com',
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
