# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ntc_rosetta_conf']

package_data = \
{'': ['*'], 'ntc_rosetta_conf': ['yang/*']}

install_requires = \
['click>=7.0,<8.0', 'jetconf', 'ntc-rosetta>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['ntc-rosetta-conf = ntc_rosetta_conf.cmd:cli']}

setup_kwargs = {
    'name': 'ntc-rosetta-conf',
    'version': '0.1.0',
    'description': 'Restconf interface for rosetta',
    'long_description': None,
    'author': 'David Barroso',
    'author_email': 'dbarrosop@dravetech.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
