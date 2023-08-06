# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bot_filler']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['bot_filler = bot_filler.cli:main']}

setup_kwargs = {
    'name': 'bot-filler',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'ryota',
    'author_email': 'ryota@42.codes',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
