# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['keios_zmq']

package_data = \
{'': ['*']}

install_requires = \
['pyzmq>=18.0,<19.0']

setup_kwargs = {
    'name': 'keios-zmq',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Leftshift One',
    'author_email': 'contact@leftshift.one',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
