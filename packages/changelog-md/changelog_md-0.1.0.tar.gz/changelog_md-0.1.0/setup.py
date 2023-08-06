# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['changelog_md']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'changelog-md',
    'version': '0.1.0',
    'description': 'A package to create changelogs for your git tracked projects.',
    'long_description': None,
    'author': 'Ruslan Sergeev',
    'author_email': 'mybox.sergeev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
