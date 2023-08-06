# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apscheduler_bundle']

package_data = \
{'': ['*']}

install_requires = \
['APScheduler>=3.7.0,<4.0.0', 'applauncher>=2.0.2,<3.0.0']

setup_kwargs = {
    'name': 'apscheduler-bundle',
    'version': '2.0.0',
    'description': 'APScheduler support for applauncher',
    'long_description': None,
    'author': 'Alvaro Garcia',
    'author_email': 'maxpowel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
