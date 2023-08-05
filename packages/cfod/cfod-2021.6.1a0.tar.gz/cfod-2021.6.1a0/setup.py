# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfod',
 'cfod.analysis',
 'cfod.analysis.filterbank',
 'cfod.analysis.intensity',
 'cfod.routines',
 'cfod.utilities']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'h5py>=3.2.1,<4.0.0',
 'healpy>=1.14.0,<2.0.0',
 'matplotlib>=3.4.2,<4.0.0',
 'msgpack-python>=0.5.6,<0.6.0',
 'numpy>=1.20.3,<2.0.0',
 'scipy>=1.6.3,<2.0.0']

extras_require = \
{'pandas': ['pandas>=1.2.4,<2.0.0']}

entry_points = \
{'console_scripts': ['msgpack2fil = cfod.routines.msgpack2fil:runner']}

setup_kwargs = {
    'name': 'cfod',
    'version': '2021.6.1a0',
    'description': 'CHIME FRB Open Data',
    'long_description': None,
    'author': 'Shiny Brar',
    'author_email': 'charanjotbrar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://chime-frb-open-data.github.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
