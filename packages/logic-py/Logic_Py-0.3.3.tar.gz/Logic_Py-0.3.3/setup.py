# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logic_py']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'logic-py',
    'version': '0.3.3',
    'description': 'PAckage to realize combinational logic gates',
    'long_description': '# Logic_Py\n\nThis Python package enables the user to realise Logic based combinational circuits built on basic logic gates.\nAll the inputs must be binary and of same length for the functions to perform desired operation. \n\n## Basic Gates\n\nThere are 7 basic gates, all other secondaary and combinational gates are the combinations of these 7 basic gates.\n- AND, OR, NOT, NAND, NOR,XNOR,XOR\n\n## Secondary Gates\n\nThere are 16 Secondary gates, which take 4 binary inputs and 1 binary output.\n- AND_AND, AND_OR, AND_NAND, AND_NOR, OR_AND, OR_OR, \n   OR_NAND, OR_NOR, NAND_AND, NAND_OR, NAND_NAND, \n   NAND_NOR, NOR_AND, NOR_OR, NOR_NAND, NOR_NOR,\n\n## Combinational Gates\nFew combinational circuits are added as start in this beta version, few more will follow in the coming update.\n- Binary2Gray, Gray2Binary, EParity_gen, EParity_check, OParity_gen, OParity_check\n\n## Arithmatic Gates\nTwo arithmatic gates are added for the beta version, more will follow in the coming update.\n- Half Adder\n- Full Adder\n\n## Plots\nPlots for the basic gates, secondary gates and arithmatic gates are available with the current version.\n- plot_full_adder, plot_half_adder, plot_secondary, plot_basic\n\n## Citation\n- [Tutorialspoint - digital circuit basics](https://www.tutorialspoint.com/digital_circuits)\n\n>Use [Github](https://github.com/vishwesh-vishwesh/Logic_Py/) for further updates. \n>Please kindly cite incase you use the package and fork.\n\n>Use Hellow world example for the syntax\n>or use help function in python console\n>ex: help(AND)\n\n',
    'author': 'Vishwesh',
    'author_email': 'vishwesh.arush@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Vishwesh-Vishwesh/Logic_Py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
