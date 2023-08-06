# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maxcutpy']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.5.1,<3.0.0',
 'numpy>=1.20.3,<2.0.0',
 'pandas>=1.2.4,<2.0.0',
 'tqdm>=4.61.0,<5.0.0']

setup_kwargs = {
    'name': 'maxcutpy',
    'version': '0.1.0',
    'description': 'A Python Implementation of Graph Max Cut Solutions',
    'long_description': None,
    'author': 'trevorWieland',
    'author_email': 'trevor_wieland@mac.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
