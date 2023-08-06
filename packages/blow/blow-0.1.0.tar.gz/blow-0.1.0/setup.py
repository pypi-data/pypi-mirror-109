# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blow']

package_data = \
{'': ['*']}

install_requires = \
['grequests>=0.6.0,<0.7.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['blow = blow:main']}

setup_kwargs = {
    'name': 'blow',
    'version': '0.1.0',
    'description': 'Small script to dos evil hackers.',
    'long_description': '# blow\n\n## Motivation\n\nLoad testing a page quickly.\n\n## Installation\n\n```\npip install blow\n```\n\n## Usage\n\n```\nblow --method get --factor 123 https://example.com\n```\n\n## License\n\nThis project is licensed under the GPL-3 license.\n',
    'author': '4thel00z',
    'author_email': '4thel00z@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
