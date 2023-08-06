# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tog']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'docopt>=0.6.2,<0.7.0',
 'psycopg2-binary>=2.8.5,<3.0.0',
 'pydash>=4.7.6,<5.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pytz>=2020.1,<2021.0',
 'tqdm>=4.46.0,<5.0.0']

entry_points = \
{'console_scripts': ['tog = tog.cli:main']}

setup_kwargs = {
    'name': 'tog',
    'version': '0.3.0',
    'description': 'Command line tool for interacting with tog data server',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
