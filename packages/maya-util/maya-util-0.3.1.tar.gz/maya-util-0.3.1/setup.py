# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mayautil']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'maya-util',
    'version': '0.3.1',
    'description': 'Utilities for working with the Maya API.',
    'long_description': None,
    'author': 'Mitchell Coote',
    'author_email': 'mitchellcoote@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
