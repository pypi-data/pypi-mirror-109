# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['salt_lsp']

package_data = \
{'': ['*'], 'salt_lsp': ['data/*']}

install_requires = \
['PyYAML>=5.4,<6.0', 'pygls>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['dump_state_name_completions = '
                     'salt_lsp.cmds:dump_state_name_completions',
                     'salt_lsp_server = salt_lsp.__main__:main']}

setup_kwargs = {
    'name': 'salt-lsp',
    'version': '0.0.1',
    'description': 'Salt Language Server Protocol Server',
    'long_description': None,
    'author': 'Dan Čermák',
    'author_email': 'dcermak@suse.com',
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
