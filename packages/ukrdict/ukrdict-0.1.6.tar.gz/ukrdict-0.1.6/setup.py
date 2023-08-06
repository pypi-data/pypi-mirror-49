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
    'version': '0.1.6',
    'description': 'CLI tool for looking up Ukrainian words meaning.',
    'long_description': "ukrdict\n=======\n\nPython wrapper for `sum.in.ua/api <http://sum.in.ua/api>`__\n\nSearch for the word meaning\n'''''''''''''''''''''''''''\n\n.. code:: bash\n\n   ukrdict лелека\n\n::\n\n   ЛЕЛЕ́КА, и, чол. і жін. Великий перелітний птах із\n   довгим прямим дзьобом та довгими ногами. Доля\n   Жабам догодила — Лелеку королем зробила (Леонід Глібов, Вибр.,\n   1951, 123); На високому стовбурі старого в'яза в лелечім\n   гнізді сплять лелеки — самець і самка (Олександр Довженко, I, 1958,\n   85); — Недарма на моїй хаті звили гніздо лелеки.. —\n   Лелеки — то щастя! (Михайло Стельмах, II, 1962, 291); //\xa0\n   рідко. Про такого птаха-самця. На старій вербі похилій,\n   під дощем і спекою, Жила собі лелечиха із лелекою\n   (Іван Нехода, Ми живемо.., 1960, 31); \xa0*\xa0Образно. Кохай мене,\n   я твій завжди, незмінна подруго далека. Моя зажурена\n   лелеко, прилинь сюди! (Микола Упеник, Вірші.., 1957, 26); \xa0*\xa0У\xa0порівняннях. Ось вони розійшлися у ланцюг. Хороші хлопці,\n   чорт візьми! Бачать, як лелеки (Юрій Яновський, I, 1958,\n   90).\n\nInstallation\n''''''''''''\n\n1. `Create Python virtual\n   environment <https://docs.python.org/3.7/library/venv.html>`__\n2. Install ukrdict package\n\n.. code:: bash\n\n   pip install ukrdict\n   ukrdict лан\n",
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
