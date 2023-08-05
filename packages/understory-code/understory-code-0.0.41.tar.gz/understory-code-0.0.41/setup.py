# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['understory', 'understory.pkg', 'understory.pkg.licensing', 'understory.src']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0',
 'radon>=4.5.1,<5.0.0',
 'semver>=2.13.0,<3.0.0',
 'sh>=1.14.2,<2.0.0',
 'understory-term']

entry_points = \
{'console_scripts': ['pkg = understory.pkg.__main__:main']}

setup_kwargs = {
    'name': 'understory-code',
    'version': '0.0.41',
    'description': 'Tools for metamodern software development',
    'long_description': '# understory-code\nTools for metamodern software development\n\n- pkg\n- src\n',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@lahacker.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
