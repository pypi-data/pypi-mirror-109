# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['druid_libs', 'druid_libs.tests_tools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'druid-libs',
    'version': '0.1.15',
    'description': 'Python utilities for Druid projects',
    'long_description': '# Druid Libs \n![PythonSupport](https://img.shields.io/static/v1?label=python&message=3.7%20|%203.8|%203.9&color=blue?style=flat-square&logo=python) ![PyPI version](https://badge.fury.io/py/druid-libs.svg) ![PyPi monthly downloads](https://img.shields.io/pypi/dm/druid-libs)\n\nA suite of Python utilities to ease adopting best practices such as test mock lambda functions.\n\n## Features\n* **[MockLambda]()** - A utility that help you to test Lambda function handlers locally with unity test, this utility allow you invoke your lambda passing dinamically env variables to your function, to test his behavior.\n\n* **[FakeContext]()** - A utility that help you to test Lambda function handlers locally with unity test, using a fake context.\n\n* **[FakeEvent]()** - A utility that help you to create a fake event for API Gateway, this help you to work with verbs: GET, POST, DELETE, and UPDATE. \n\n### Installation\nWith [pip](https://pip.pypa.io/en/latest/index.html) installed, run: ``pip install druid-libs``\n\n## License\n\nThis library is licensed under the MIT-0 License. See the LICENSE file.',
    'author': 'Druid',
    'author_email': None,
    'maintainer': 'Geyson',
    'maintainer_email': 'geyson.ferreira@druid.com',
    'url': 'https://github.com/jasonFerre/python-lib',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
