# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['coolors']

package_data = \
{'': ['*']}

install_requires = \
['pyppeteer>=0.2.5,<0.3.0']

setup_kwargs = {
    'name': 'coolors',
    'version': '0.1.4',
    'description': 'generates 5 random colors by scraping coolors.co',
    'long_description': 'A simple package to gen a color scheme by scraping coolors.co\n\nto use import coolor function and run\n',
    'author': 'Arjun Gandhi',
    'author_email': 'account@arjugandhi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
