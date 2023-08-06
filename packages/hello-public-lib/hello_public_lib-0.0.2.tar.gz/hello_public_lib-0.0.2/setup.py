# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hello_public_lib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hello-public-lib',
    'version': '0.0.2',
    'description': 'Awesome library',
    'long_description': None,
    'author': 'Very Good Security',
    'author_email': 'dev@verygoodsecurity.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
