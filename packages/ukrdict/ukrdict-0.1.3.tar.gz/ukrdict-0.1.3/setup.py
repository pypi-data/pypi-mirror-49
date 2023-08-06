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
    'version': '0.1.3',
    'description': 'CLI tool for looking up Ukrainian words meaning.',
    'long_description': '# ukrdict\nPython wrapper for [sum.in.ua/api](http://sum.in.ua/api)\n\n##### Search for the word meaning\n```bash\nukrdict тин\n```\n```\nТИН, у, чол. Огорожа, сплетена з лози, тонкого гілля\nпліт. Та вже ж наші слобожани Тини городили; Із-під\nлугу, із-під гаю Лозу волочили (Яків Щоголів, Поезії, 1958, 130);\n```\n',
    'author': 'serhii73',
    'author_email': 'aserhii@protonmail.com',
    'url': 'https://github.com/serhii73/ukrdict',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
