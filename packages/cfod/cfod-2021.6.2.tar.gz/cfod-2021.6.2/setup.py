# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfod',
 'cfod.analysis',
 'cfod.analysis.filterbank',
 'cfod.analysis.intensity',
 'cfod.data',
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
    'version': '2021.6.2',
    'description': 'CHIME FRB Open Data',
    'long_description': '<h1 align="center">\n  <br>\n  <a href="https://chime-frb-open-data.github.io"><img src="https://github.com/chime-frb-open-data/chime-frb-open-data.github.io/blob/79d7c2d574a6c849125583395f5442333630222d/docs/static/chime-frb-logo.png" alt="" width="25%"></a>\n  <br>\n  Utililes for CHIME/FRB Open Data Releases.\n  <br>\n</h1>\n\n\n## Installation\n```\npip install --user cfod\n\n# To install with pandas support,\npip install --user cfod[pandas]\n```\n\n## Documentation\nCheck out the user documentation, [here](https://chime-frb-open-data.github.io/)\n\n\n## Developer\n```\n# cfod uses poetry for package management and virtualenv management\npip install poetry\n\ngit clone git@github.com:chime-frb-open-data/chime-frb-open-data.git\ncd chime-frb-open-data\n\n# Install git-commit hook\npoetry run pre-commit install\n\n# Make changes to the code and open a PR\n```\n\n## Removal\n```\npip uninstall cfod\n```\n\n\n<p align="center">\n  <a href="Some Love">\n    <img src="https://forthebadge.com/images/badges/built-with-love.svg">\n  </a>\n</p>\n',
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
