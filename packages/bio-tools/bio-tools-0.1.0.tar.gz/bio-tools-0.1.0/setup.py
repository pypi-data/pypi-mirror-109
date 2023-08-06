# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bio_tools']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.4,<2.0.0']

setup_kwargs = {
    'name': 'bio-tools',
    'version': '0.1.0',
    'description': 'Tools for computational biology',
    'long_description': None,
    'author': 'Luke Schiefelbein',
    'author_email': 'luke.schiefelbein@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
