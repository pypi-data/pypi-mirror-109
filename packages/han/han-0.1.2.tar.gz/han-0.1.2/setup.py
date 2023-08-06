# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['han']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'han',
    'version': '0.1.2',
    'description': 'aaaaaaaaaa',
    'long_description': '\n# han\n![PyPI](https://img.shields.io/pypi/v/han?style=plastic)\n\nhan = 汉    \nhan = 汉(字) \n\n一个python常用函数库，里面的函数都是中文汉字\n\n>该项目翻译了部分函数，但没有对原函数做任何修改,不会影响你以前的代码      \n>该项目并非生硬的翻译python标准库，而是在某些地方做了修改，减少歧义，   \n>如 `round()` 是python里做四舍五入运算的，   \n>`round(1.675, 2)` # 返回值 1.68，小数部分是68    \n>`round(2.675, 2)` # 返回值 2.67，小数部分是67    \n>返回值里的最后一位小数点则充满了歧义，一个是8,一个是7，违反了人类直觉    \n>\n>而本项目的函数  `四舍五入()` 则没有这种违反直觉的歧义， \n>\n>你可以根据自己的需要使用本项目的 `四舍五入()` 或者用python自带的 `round()`\n>\n>注：经过简单测试，在以下语言中，round函数的返回值是符合直觉的，这让我们有底气重写 `四舍五入()` :    \n>php（round）、c++（round）、c#（Math.Round）、office Excel(round)      \n>其他语言，软件 没有测试，不太懂\n \n \n \n## 使用前提:\n * python > 3.8+ （3.8以上的版本）\n\n## 安装\n\n`pip install han`\n\n## 用法\n\n```python\nfrom han.数学 import *\n\n求绝对值(-123)\n \n```\n\n## 文档\n\ngitee（速度快） https://xxxxx.com   \ngithub（速度慢） https://xxxxx.com   \n\n\n\n## 测试\n 1、下载代码到本地,进入代码根目录    \n 2、执行 `pip install poetry `   \n 3、执行 `poetry install`   \n 4、执行 `pytest`    \n\n ',
    'author': 'piqizhu',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/piqizhu/han',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
