# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acopoweropt']

package_data = \
{'': ['*']}

install_requires = \
['cvxopt>=1.2.6,<2.0.0', 'pandas>=1.2.4,<2.0.0']

setup_kwargs = {
    'name': 'acopoweropt',
    'version': '0.1.0',
    'description': 'Ant Colony Power Systems Optimizer',
    'long_description': '# Ant Colony Power Systems Optimizer\n\nThis library aims to provide a tool to solve an optimal dispach of Thermal Generation Units, using the Ant Colony Optimization algorithm, hence the library name acopoweropt (**A**nt **Co**lony **Power** **Opt**imizer)\n\n> This is an under development library',
    'author': 'Ettore Aquino',
    'author_email': 'ettore@ettoreaquino.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ettoreaquino/acopoweropt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
