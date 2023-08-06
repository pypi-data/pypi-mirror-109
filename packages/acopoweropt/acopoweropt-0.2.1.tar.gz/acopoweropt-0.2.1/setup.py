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
    'version': '0.2.1',
    'description': 'Ant Colony Power Systems Optimizer',
    'long_description': '[![PyPI version](https://badge.fury.io/py/acopoweropt.svg)](https://badge.fury.io/py/acopoweropt)\n\n# Ant Colony Power Systems Optimizer\n\nThis library aims to provide a tool to obtain an optimal dispach of a Power System comprised of Thermal Generation Units. The approach combines the Ant Colony Optimizer with a non-linear solver provided by CVXOPT.\n\n> This is an under development library\n\n## Installation instructions\n\n### PyPi\nA pre-built binary wheel package can be installed using pip:\n```sh\npip install acopoweropt\n```\n\n### Poetry\nPoetry is a tool for dependency management and packaging in Python. `acopoweropt` can be installed in a poetry managed project:\n```sh\npoetry add acopoweropt\n```\n\n## Usage\nFrom a domain perspective, there should be a complete decoupling between an Ant Colony and a Power System, after all ants do not have knowledge of power systems. Therefore an initial approach was to develop to main _Entities_: A `Colony` and a `Power System`. A Power System should be solved by a mathematical method which might achieve a global optimal result or not.\n\nSince the dispach of "multi operative zone" Thermal Generation Units (TGUs) bring non linearities to the formulation, obtaining a global optimal financial dispach of the system is not a trivial task. The Ant Colony algorithm came in hand as a tool to iteractively seek a global optimal result without having to rely on brute computational force.\n\n### Defining Systems\nThe systems configuration should be defined in the [`systems.json`](systems.json) file. In the example provided, 3 systems where defined: \'s10\', \'s15\' and \'s40\', the names were chosen for convention and will be used by the `PowerSystem` class to initialize the desired configuration.\n\n\n#### Example\n\nThe code below samples a possible configuration which can be used to operate the system and solves this configuration.\n\n```python\nfrom acopoweropt import system\n\n# Intance a PowerSystem class from a configuration file where \'s10` defines a system configuration\nPSystem = system.PowerSystem(name=\'s10\')\n\n# Randomly selects a possible system operation (there are cases where more than a single unit can be operated in diferent configurations)\noperation = PSystem.sample_operation()\n\n# Solve the Economic Dispatch of the units of a specific configuration of the system, in this case, let\'s use the previously sampled one:\nsolution = PSystem.solve(operation=operation)\n\n# Prints total financial cost of the operation\nprint("Total Financial Cost: {}".format(solution.get(\'Ft\')))\n\n# Prints the operation with its power dispach values\nprint(solution.get(\'operation\'))\n```\n\nAnother option is to bring your own sequence of operative zones (1 for each TGU) and build the operation data from it:\n\n```python\nfrom acopoweropt import system\n\n# Intance a PowerSystem class from a configuration file where \'s10` defines a system configuration\nPSystem = system.PowerSystem(name=\'s10\')\n\n# Define a sequence of operative zones for each of the 10 TGUs\nopzs = [2, 3, 1, 2, 1, 1, 3, 1, 1, 3]\n\n# Build a configuration that represents such sequence of operative zones\noperation = PSystem.get_operation(operative_zones=opzs)\n\n# Solve the Economic Dispatch of the specific configuration:\nsolution = PSystem.solve(operation=operation)\n\n# Prints total financial cost of the operation\nprint("Total Financial Cost: {}".format(solution.get(\'Ft\')))\n\n# Prints the operation with its power dispach values\nprint(solution.get(\'operation\'))\n```\n\n### Defining Colonies\nAn Ant Colony should seek for a global optimal solution or "the optimal source of food". The algorithm was proposed by Marco Dorigo, check [Wiki](https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms) for more details.\n\n#### Example\n\nThe code below initializes a colony with a sample operation of our power system.\n\n```python\nfrom acopoweropt import colony, system\n\n# Intance a Colony class which will use the \'s10` Power System to initialize random paths for the colony to seek\n\nColony = colony.Colony(n_ants=5, phr_evp_rate=0.25, power_system_name=\'s10\')\nColony.initialize()\n\nprint(Colony.initial_paths)\n```\n\n## License\n\nSee the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).',
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
