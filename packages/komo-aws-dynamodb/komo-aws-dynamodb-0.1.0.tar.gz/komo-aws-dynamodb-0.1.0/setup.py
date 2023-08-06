# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['komo_aws_dynamodb']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.94,<2.0.0']

setup_kwargs = {
    'name': 'komo-aws-dynamodb',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Khosi',
    'author_email': 'khosimorafo@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
