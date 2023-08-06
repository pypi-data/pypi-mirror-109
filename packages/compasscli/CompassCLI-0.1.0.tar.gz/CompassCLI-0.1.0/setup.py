# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['compasscli']

package_data = \
{'': ['*']}

install_requires = \
['ZypeSDK>=1.6,<2.0', 'rich>=10.3.0,<11.0.0']

entry_points = \
{'console_scripts': ['compass = compasscli.compass:main']}

setup_kwargs = {
    'name': 'compasscli',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Rajdeep Malakar',
    'author_email': 'Rajdeep@tgeeks.cf',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
