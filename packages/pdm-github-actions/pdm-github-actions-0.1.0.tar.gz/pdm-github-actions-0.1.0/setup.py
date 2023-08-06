# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bogus']

package_data = \
{'': ['*']}

install_requires = \
['fastapi[webapi]>=0.65.2,<0.66.0',
 'requests>=2.25.1,<3.0.0',
 'typer>=0.3.2,<0.4.0',
 'uvicorn[webapi]>=0.14.0,<0.15.0']

entry_points = \
{'console_scripts': ['bogus = bogus.main:cli']}

setup_kwargs = {
    'name': 'pdm-github-actions',
    'version': '0.1.0',
    'description': 'A GitHub Actions demo focused on python',
    'long_description': None,
    'author': 'JnyJny',
    'author_email': 'erik.oshaughnessy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
