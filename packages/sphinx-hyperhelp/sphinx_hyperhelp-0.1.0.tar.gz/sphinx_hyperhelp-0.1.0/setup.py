# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_hyperhelp']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=4.0.2,<5.0.0', 'sphinxcontrib-websupport>=1.2.4,<2.0.0']

entry_points = \
{'sphinx.builders': ['hyperhelp = sphinx_hyperhelp']}

setup_kwargs = {
    'name': 'sphinx-hyperhelp',
    'version': '0.1.0',
    'description': 'Builder for Sphinx documentation, to the HyperHelp format, for Sublime Text reading',
    'long_description': None,
    'author': 'Guillaume Wenzek',
    'author_email': None,
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
