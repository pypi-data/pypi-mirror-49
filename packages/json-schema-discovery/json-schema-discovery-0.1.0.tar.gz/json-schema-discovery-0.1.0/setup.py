# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['json_schema_discovery']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'json-schema-discovery',
    'version': '0.1.0',
    'description': 'Database-agnostic JSON schema discovery',
    'long_description': None,
    'author': 'Stepland',
    'author_email': 'Stepland@hotmail.fr',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
