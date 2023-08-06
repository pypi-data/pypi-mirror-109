# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clickhouse_pool']

package_data = \
{'': ['*']}

install_requires = \
['clickhouse-driver>=0.2.1,<0.3.0']

setup_kwargs = {
    'name': 'clickhouse-pool',
    'version': '0.5.0',
    'description': 'a thread-safe connection pool for ClickHouse',
    'long_description': None,
    'author': 'Eric McCarthy',
    'author_email': 'ericmccarthy7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
