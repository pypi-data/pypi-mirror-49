# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aioli_guestbook', 'aioli_guestbook.service']

package_data = \
{'': ['*']}

install_requires = \
['aioli>=0.3.1,<0.4.0',
 'aioli_rdbms>=0.1.3,<0.2.0',
 'maxminddb-geolite2>=2018.703,<2019.0',
 'toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'aioli-guestbook',
    'version': '0.1.4',
    'description': 'Comprehensive RESTful HTTP API built on top of the Aioli Framework',
    'long_description': 'aioli-guestbook: RESTful HTTP API Example\n---\n\nThe idea with this example is to show how a CRUD-type RESTful HTTP API package can be built with the Aioli Framework.\n\n\nDocumentation\n---\n\nCheck out the [Package Documentation](https://aioli-guestbook-example.readthedocs.io) for usage and info about the\nHTTP and Service APIs.\n\nAuthor\n---\nRobert Wikman \\<rbw@vault13.org\\>\n\n',
    'author': 'Robert Wikman',
    'author_email': 'rbw@vault13.org',
    'url': 'https://github.com/aioli-framework/aioli-guestbook-example',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
