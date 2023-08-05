# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wdiff']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=0.25,<0.26']

setup_kwargs = {
    'name': 'wdiff',
    'version': '0.0.8',
    'description': 'Analyze how difficult a Spanish word will be to spell',
    'long_description': None,
    'author': 'Mario E. Bermonti Pérez',
    'author_email': 'mbermonti1132@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
