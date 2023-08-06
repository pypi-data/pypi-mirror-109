# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xortool_ciphey']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0']

setup_kwargs = {
    'name': 'xortool-ciphey',
    'version': '0.1.14',
    'description': 'Multi-byte xor analysis for Ciphey',
    'long_description': None,
    'author': 'bee-san',
    'author_email': 'github@skerritt.blog',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
