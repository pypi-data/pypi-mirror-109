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
    'version': '0.2.0',
    'description': 'Ant Colony Power Systems Optimizer',
    'long_description': '[![PyPI version](https://badge.fury.io/py/acopoweropt.svg)](https://badge.fury.io/py/acopoweropt)\n\n# Ant Colony Power Systems Optimizer\n\nThis library aims to provide a tool to obtain an optimal dispach of a Power System comprised of Thermal Generation Units. The approach combines the Ant Colony Optimizer with a non-linear solver provided by CVXOPT.\n\n> This is an under development library\n\n## Installation instructions\n\n### PyPi\nA pre-built binary wheel package can be installed using pip:\n```sh\npip install acopoweropt\n```\n\n### Poetry\nPoetry is a tool for dependency management and packaging in Python. `acopoweropt` can be installed in a poetry managed project:\n```sh\npoetry add acopoweropt\n```\n\n## Usage\nFrom a domain perspective, there should be a complete decoupling between an Ant Colony and a Power System, after all ants do not have knowledge of power systems. Therefore an initial approach was to develop to main _Entities_: A `Colony` and a `Power System`. A Power System should be solved by a mathematical method which might can be or not the optimal result, which is where the Ant Colony Algorithm can be used.\n\n### Defining Systems\nThe systems configuration should be defined in the [`systems.json`](systems.json) file. In the example provided, 3 systems where defined: \'s10\', \'s15\' and \'s40\', the names were chosen for convention and will be used by the `PowerSystem` class to initialize the desired configuration.\n\n\n### Example\n\n```python\nfrom acopoweropt import system\n\n# Intance a PowerSystem class from a configuration file where \'s10` defines a\n# system configuration\nPSystem = system.PowerSystem(name=\'s10\')\n\n# Randomly selects a possible system operation (there are cases where more than\n# a single unit can be operated in diferent configurations)\noperation = PSystem.sample_operation()\n\n# Solve the Economic Dispatch of the units of a specific configuration of the\n# system, in this case, let\'s use the previously sampled one:\nsolution = PSystem.solve(operation=operation)\n\n# Prints total financial cost of the operation\nprint("Total Financial Cost: {}".format(solution.get(\'Ft\')))\n\n# Prints the operation with its power dispach values\nprint(solution.get(\'operation\'))\n```\n\n## License\n\nSee the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).',
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
