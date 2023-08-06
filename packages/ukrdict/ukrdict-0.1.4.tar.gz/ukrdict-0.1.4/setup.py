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
    'version': '0.1.4',
    'description': 'CLI tool for looking up Ukrainian words meaning.',
    'long_description': "`Maintenance <https://GitHub.com/serhii73/ukrdict/graphs/commit-activity>`__\n`made-with-python <https://www.python.org/>`__\n`made-with-python <https://github.com/python/black>`__ `GitHub\ncontributors <https://GitHub.com/serhii73/ukrdict/graphs/contributors/>`__\n`GitHub stars <https://GitHub.com/serhii73/ukrdict/stargazers/>`__\n|GitHub forks| `GitHub\nissues <https://GitHub.com/serhii73/ukrdict/issues/>`__ `Build\nStatus <https://travis-ci.org/serhii73/ukrdict>`__\n`Maintainability <https://codeclimate.com/github/serhii73/ukrdict/maintainability>`__\n`BCH compliance <https://bettercodehub.com/>`__ `Total\nalerts <https://lgtm.com/projects/g/serhii73/ukrdict/alerts/>`__\n`Language grade:\nPython <https://lgtm.com/projects/g/serhii73/ukrdict/context:python>`__\n`Codacy\nBadge <https://app.codacy.com/app/serhii73/ukrdict?utm_source=github.com&utm_medium=referral&utm_content=serhii73/ukrdict&utm_campaign=Badge_Grade_Settings>`__\n`Python 3 <https://pyup.io/repos/github/serhii73/ukrdict/>`__\n`Updates <https://pyup.io/repos/github/serhii73/ukrdict/>`__\n\nukrdict\n=======\n\nPython wrapper for `sum.in.ua/api <http://sum.in.ua/api>`__\n\nSearch for the word meaning\n'''''''''''''''''''''''''''\n\n.. code:: bash\n\n   ukrdict тин\n\n::\n\n   ТИН, у, чол. Огорожа, сплетена з лози, тонкого гілля\n   пліт. Та вже ж наші слобожани Тини городили; Із-під\n   лугу, із-під гаю Лозу волочили (Яків Щоголів, Поезії, 1958, 130);\n\nInstallation\n''''''''''''\n\n1. Clone the repository\n2. `Create Python virtual\n   environment <https://docs.python.org/3.7/library/venv.html>`__\n3. Install ukrdict package\n\n.. code:: bash\n\n   pip install ukrdict\n   ukrdict жовтогарячий\n\n.. |GitHub forks| image:: https://img.shields.io/github/forks/serhii73/ukrdict.svg?style=social\n\n",
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
