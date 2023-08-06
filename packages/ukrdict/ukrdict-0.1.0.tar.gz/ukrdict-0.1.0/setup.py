# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ukrdict']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4==4.7.1', 'click==7.0', 'lxml==4.3.4', 'requests==2.22.0']

entry_points = \
{'console_scripts': ['ukrdict = ukrdict.__main__:main']}

setup_kwargs = {
    'name': 'ukrdict',
    'version': '0.1.0',
    'description': 'CLI tool for looking up Ukrainian words meaning.',
    'long_description': None,
    'author': 'serhii73',
    'author_email': 'aserhii@protonmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
