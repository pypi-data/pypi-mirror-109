# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['understory',
 'understory.indieweb',
 'understory.indieweb.indieauth',
 'understory.indieweb.indieauth.templates',
 'understory.indieweb.micropub',
 'understory.indieweb.micropub.templates',
 'understory.indieweb.microsub',
 'understory.indieweb.microsub.templates',
 'understory.indieweb.templates',
 'understory.indieweb.webmention',
 'understory.indieweb.websub']

package_data = \
{'': ['*'],
 'understory.indieweb.webmention': ['templates/*'],
 'understory.indieweb.websub': ['templates/*']}

install_requires = \
['understory-web>=0.0.19,<0.0.20']

entry_points = \
{'console_scripts': ['loveliness = understory.loveliness:main']}

setup_kwargs = {
    'name': 'understory',
    'version': '0.0.33',
    'description': 'The tools that power the canopy',
    'long_description': '# understory\nThe tools that power the canopy\n\n## Install\n\n    pip install understory\n',
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
