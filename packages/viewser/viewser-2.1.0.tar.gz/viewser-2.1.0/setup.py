# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['viewser', 'viewser.tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'crayons>=0.4.0,<0.5.0',
 'environs>=9.3.1,<10.0.0',
 'fitin>=0.2.0,<0.3.0',
 'pandas>=1.2.3,<2.0.0',
 'pyarrow>=3.0.0,<4.0.0',
 'pydantic>=1.8.1,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'toml>=0.10.2,<0.11.0',
 'toolz>=0.11.1,<0.12.0',
 'views-schema>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['viewser = viewser.cli:viewser']}

setup_kwargs = {
    'name': 'viewser',
    'version': '2.1.0',
    'description': '',
    'long_description': None,
    'author': 'peder2911',
    'author_email': 'pglandsverk@gmail.com',
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
