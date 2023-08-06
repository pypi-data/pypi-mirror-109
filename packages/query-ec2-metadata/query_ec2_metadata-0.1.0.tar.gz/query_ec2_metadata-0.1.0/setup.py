# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['query_ec2_metadata']
install_requires = \
['requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['ec2-metadata = query_ec2_metadata:main',
                     'instance-identity = query_ec2_metadata:main']}

setup_kwargs = {
    'name': 'query-ec2-metadata',
    'version': '0.1.0',
    'description': 'Allows querying EC2 instance metadata',
    'long_description': None,
    'author': 'HMRC WebOps',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
