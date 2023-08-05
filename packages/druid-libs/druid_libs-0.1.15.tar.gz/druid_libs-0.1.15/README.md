# Druid Libs 
![PythonSupport](https://img.shields.io/static/v1?label=python&message=3.7%20|%203.8|%203.9&color=blue?style=flat-square&logo=python) ![PyPI version](https://badge.fury.io/py/druid-libs.svg) ![PyPi monthly downloads](https://img.shields.io/pypi/dm/druid-libs)

A suite of Python utilities to ease adopting best practices such as test mock lambda functions.

## Features
* **[MockLambda]()** - A utility that help you to test Lambda function handlers locally with unity test, this utility allow you invoke your lambda passing dinamically env variables to your function, to test his behavior.

* **[FakeContext]()** - A utility that help you to test Lambda function handlers locally with unity test, using a fake context.

* **[FakeEvent]()** - A utility that help you to create a fake event for API Gateway, this help you to work with verbs: GET, POST, DELETE, and UPDATE. 

### Installation
With [pip](https://pip.pypa.io/en/latest/index.html) installed, run: ``pip install druid-libs``

## License

This library is licensed under the MIT-0 License. See the LICENSE file.