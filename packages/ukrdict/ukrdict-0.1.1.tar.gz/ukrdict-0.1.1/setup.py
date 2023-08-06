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
    'version': '0.1.1',
    'description': 'CLI tool for looking up Ukrainian words meaning.',
    'long_description': '[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/serhii73/ukrdict/graphs/commit-activity)\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)\n[![made-with-python](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)\n[![GitHub contributors](https://img.shields.io/github/contributors/serhii73/ukrdict.svg)](https://GitHub.com/serhii73/ukrdict/graphs/contributors/)\n[![GitHub stars](https://img.shields.io/github/stars/serhii73/ukrdict.svg?style=social&label=Star&maxAge=2592000)](https://GitHub.com/serhii73/ukrdict/stargazers/)\n![GitHub forks](https://img.shields.io/github/forks/serhii73/ukrdict.svg?style=social)\n[![GitHub issues](https://img.shields.io/github/issues/serhii73/ukrdict.svg)](https://GitHub.com/serhii73/ukrdict/issues/)\n[![Build Status](https://travis-ci.org/serhii73/ukrdict.svg?branch=master)](https://travis-ci.org/serhii73/ukrdict)\n[![Maintainability](https://api.codeclimate.com/v1/badges/18c3e844245a2585f912/maintainability)](https://codeclimate.com/github/serhii73/ukrdict/maintainability)\n[![BCH compliance](https://bettercodehub.com/edge/badge/serhii73/ukrdict?branch=master)](https://bettercodehub.com/)\n[![Total alerts](https://img.shields.io/lgtm/alerts/g/serhii73/ukrdict.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/serhii73/ukrdict/alerts/)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/serhii73/ukrdict.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/serhii73/ukrdict/context:python)\n[![Codacy Badge](https://api.codacy.com/project/badge/Grade/007ff2464e874948add4154dc0f97e35)](https://app.codacy.com/app/serhii73/ukrdict?utm_source=github.com&utm_medium=referral&utm_content=serhii73/ukrdict&utm_campaign=Badge_Grade_Settings)\n[![Python 3](https://pyup.io/repos/github/serhii73/ukrdict/python-3-shield.svg)](https://pyup.io/repos/github/serhii73/ukrdict/)\n[![Updates](https://pyup.io/repos/github/serhii73/ukrdict/shield.svg)](https://pyup.io/repos/github/serhii73/ukrdict/)\n\n# ukrdict\nPython wrapper for [sum.in.ua/api](http://sum.in.ua/api)\n\n##### Search for the word meaning\n```bash\nukrdict тин\n```\n```\nТИН, у, чол. Огорожа, сплетена з лози, тонкого гілля\nпліт. Та вже ж наші слобожани Тини городили; Із-під\nлугу, із-під гаю Лозу волочили (Яків Щоголів, Поезії, 1958, 130);\n```\n\n##### Installation\n1. Clone the repository\n2. [Create Python virtual environment](https://docs.python.org/3.7/library/venv.html)\n3. Install ukrdict package\n```bash\npip install ukrdict\nukrdict жовтогарячий\n```\n',
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
