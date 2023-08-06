# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pretty_plz']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['plz = pretty_plz.main:main']}

setup_kwargs = {
    'name': 'pretty-plz',
    'version': '0.1.3',
    'description': 'pretty_plz is a tool that turns utility scripts into runnable commands',
    'long_description': None,
    'author': 'Tamás Szelei',
    'author_email': 'szelei.t@gmail.com',
    'url': 'https://github.com/sztomi/pretty_plz/',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
