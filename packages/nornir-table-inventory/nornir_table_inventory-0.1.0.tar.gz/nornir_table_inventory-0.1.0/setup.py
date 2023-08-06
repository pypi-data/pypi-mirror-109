# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_table_inventory',
 'nornir_table_inventory.plugins',
 'nornir_table_inventory.plugins.inventory']

package_data = \
{'': ['*']}

install_requires = \
['nornir>=3.1.1,<4.0.0', 'pandas>=1.2.4,<2.0.0']

entry_points = \
{'nornir.plugins.inventory': ['CSVInventory = '
                              'nornir_table_inventory.plugins.inventory.table:CSVInventory',
                              'ExcelInventory = '
                              'nornir_table_inventory.plugins.inventory.table:ExcelInventory']}

setup_kwargs = {
    'name': 'nornir-table-inventory',
    'version': '0.1.0',
    'description': 'nornir inventory plugin,support managing of inventory by csv or excel file',
    'long_description': None,
    'author': 'feifeiflight',
    'author_email': 'feifeiflight@126.com',
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
