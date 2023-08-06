# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['resistics_readers',
 'resistics_readers.lemi',
 'resistics_readers.metronix',
 'resistics_readers.spam']

package_data = \
{'': ['*']}

install_requires = \
['defusedxml>=0.7.1,<0.8.0',
 'loguru>=0.5.3,<0.6.0',
 'numpy>=1.20.3,<2.0.0',
 'obspy>=1.2.2,<2.0.0',
 'pandas>=1.2.4,<2.0.0',
 'resistics==1.0.0a0']

setup_kwargs = {
    'name': 'resistics-readers',
    'version': '0.1.0',
    'description': 'Package with various instrument data format readers for resistics',
    'long_description': '## Welcome\n\nResistics readers is an extension to resistics adding support for various\ninstrument data formats.\n\nMore coming soon...\n',
    'author': 'Neeraj Shah',
    'author_email': 'resistics@outlook.com',
    'maintainer': 'Neeraj Shah',
    'maintainer_email': 'resistics@outlook.com',
    'url': 'https://github.com/resistics/resistics-readers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.10',
}


setup(**setup_kwargs)
