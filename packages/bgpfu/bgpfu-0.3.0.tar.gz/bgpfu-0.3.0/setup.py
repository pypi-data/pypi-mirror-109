# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bgpfu', 'bgpfu.irr', 'bgpfu.prefixlist']

package_data = \
{'': ['*'], 'bgpfu': ['templates/*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0',
 'click>=7.1.2,<8.0.0',
 'gevent>=21.1.2,<22.0.0',
 'munge>=1.1.0,<2.0.0',
 'py-radix>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['bgpfu = bgpfu.cli:cli']}

setup_kwargs = {
    'name': 'bgpfu',
    'version': '0.3.0',
    'description': 'BGP toolkit',
    'long_description': '\n[![PyPI](https://img.shields.io/pypi/v/bgpfu.svg?maxAge=60)](https://pypi.python.org/pypi/bgpfu)\n[![PyPI](https://img.shields.io/pypi/pyversions/bgpfu.svg?maxAge=600)](https://pypi.python.org/pypi/bgpfu)\n[![Tests](https://github.com/bgpfu/bgpfu/workflows/tests/badge.svg)](https://github.com/bgpfu/bgpfu)\n[![Codecov](https://img.shields.io/codecov/c/github/bgpfu/bgpfu/master.svg?maxAge=60)](https://codecov.io/github/bgpfu/bgpfu)\n\n\n# BGP FU\n\n![BGPFU](/../gh-pages/images/BGP-FU-Logo-RGB-resized.png?raw=true)\n\nBGP FU is a toolbelt to assist with the automatic creation of safe prefix-filters.\n\nBGP FU can ingest data from various sources such as IRRs/RPKI/other, transpose those\naccording to your policy preferences, and generate partial router configurations.\n\nThe jinja2 templating language is used to describe vendor specific output.\n\n## Contact\n\nJoin us on `irc.terahertz.net` in `#BGPFU`\n',
    'author': 'Matt Griswold',
    'author_email': 'grizz@20c.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bgpfu/bgpfu/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
