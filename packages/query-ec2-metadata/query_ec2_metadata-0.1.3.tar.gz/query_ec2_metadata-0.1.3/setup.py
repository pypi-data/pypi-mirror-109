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
    'version': '0.1.3',
    'description': 'Allows querying EC2 instance metadata',
    'long_description': '# EC2 Instance Metadata\n\nThis allows querying EC2 instance metadata.\n\nIt uses IMDSv2. Session credentials are NOT available using this.\n\n## Installation\n\nAvailable on Pypi as [query-ec2-metadata](https://pypi.org/project/query-ec2-metadata/) \n\n  `pip install query-ec2-metadata`\n\n## Command line tools\n\n### ec2-metadata\n\nUsage:\n  `ec2-metadata KEY`\n\n  This returns an attribute from the instance metadata.\n\n  The KEY can be any of the data values from https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-categories.html\n\n### instance-identity\n\nUsage:\n  `instance-identity KEY`\n\n  This returns an attribute from the instance identity document.\n\n  The key can be any of the data values from https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-identity-documents.html\n\n## Python module\n\n### instance_identity_document() -> Dict[str, str]:\n    \nThis returns the identity document for the instance.\n\n### instance_identity(key: str) -> str:\n   \nThis returns an attribute from the instance identity document.\n\nThe key can be any of the data values from https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-identity-documents.html\n\n### ec2_metadata(key: str) -> str:\n\nThis returns an attribute from the instance metadata.\n\nThe key can be any of the data values from https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-categories.html\n\n### Development\n\n* `make init` to set things up  \n* `make pytest` to run unit tests  \n* `make test` to run all tests  \n\nRemember to bump the version in `pyproject.toml` before merging.',
    'author': 'HMRC WebOps',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hmrc/ec2_metadata',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
