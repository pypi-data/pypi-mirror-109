# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telethon_bot', 'telethon_bot.handlers']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.2.0,<9.0.0',
 'Telethon>=1.21.1,<2.0.0',
 'cryptg>=0.2.post4,<0.3',
 'python-dotenv>=0.17.1,<0.18.0',
 'rich>=10.3.0,<11.0.0']

entry_points = \
{'console_scripts': ['telethon-bot = telethon_bot.bot:main']}

setup_kwargs = {
    'name': 'telethon-bot',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'aahnik',
    'author_email': 'daw@aahnik.dev',
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
