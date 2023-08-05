# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tweet']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.15.0,<0.16.0',
 'python-twitter>=3.5,<4.0',
 'rich>=10.2.2,<11.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['tweet = tweet.main:app']}

setup_kwargs = {
    'name': 'tweet',
    'version': '1.2.1',
    'description': 'Tweet Only Library',
    'long_description': '<p align="center">\n  <img width="200" src="static/logo.png">\n</p>\n\n---\n\n`tweet` can tweet your current status from CLI easily.\n\n`tweet` cat tweet `only`, therefore you will not be distracted.\n\n## How to Install\n\n[pipx](https://github.com/pypa/pipx) is good for running python applications in isolated environments.\n\n```\npipx install tweet\n```\n\n## How to Use\n\n```\n# Post Tweet\ntweet tweet `your-status`\n\n# Endless Mode\ntweet endless\n```\n\n## How to set up\n\nYou have to set up `~/.twitter-env` file to your home directory yourself.\nYou get tokens from [Twitter Developer](https://developer.twitter.com/en/portal/projects-and-apps).\n\n`~/.twitter-env`\n\n```env\nCONSUMER_TOKEN=.......\nCONSUMER_SECRET=.......\nACCESS_TOKEN=.......\nACCESS_SECRET=.....\n```\n',
    'author': 'ganariya',
    'author_email': 'ganariya2525@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Ganariya/tweet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
