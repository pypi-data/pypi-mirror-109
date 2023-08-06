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
    'version': '0.1.3',
    'description': 'Official CLI for Zype.',
    'long_description': '.. Zype Documentation\n\n=======================\nCompass CLI for Python3\n=======================\n\n.. code-block:: shell\n\n   pip install CompassCLI\n\nYou can see complete ZypeLang Documentation at `ZypeLang Docs <https://zype-lang.cf>`_ .\n\nFor detailed article please visit **zUbuntu** `here <https://zubuntu.zype.cf>`_ .\n\nInstallation\n************\n\nWindows\n-------\n\n.. code-block:: shell\n\n    pip install CompassCLI\n\nLinux / macOS\n-------------\n\n.. code-block:: shell\n\n    python3 -m pip install CompassCLI\n\nIf you had any problem please mail us at `TGMail <mailto:Zype@tgeeks.cf>`_ .',
    'author': 'Rajdeep Malakar',
    'author_email': 'Rajdeep@tgeeks.cf',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
