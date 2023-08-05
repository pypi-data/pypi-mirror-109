# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rocshelf',
 'rocshelf.compile',
 'rocshelf.components',
 'rocshelf.daemon',
 'rocshelf.frontend',
 'rocshelf.integration',
 'rocshelf.template']

package_data = \
{'': ['*'],
 'rocshelf': ['source/*',
              'source/defaults/*',
              'source/groups/*',
              'source/groups/material/*',
              'source/groups/tools/*',
              'source/groups/tools/blocks/info/*',
              'source/groups/tools/tags/modals/*',
              'source/layouts/*',
              'source/layouts/block/*',
              'source/layouts/page/*',
              'source/layouts/tag/*',
              'source/layouts/wrapper/*']}

install_requires = \
['Pillow>=8.2.0,<9.0.0',
 'beautifulsoup4==4.9.3',
 'libsass==0.20.1',
 'pyyaml==5.4.1',
 'rcore==0.1.4',
 'rlogging==0.1.4']

setup_kwargs = {
    'name': 'rocshelf',
    'version': '0.1.4',
    'description': 'Препроцессор для компиляции веб-страниц из составляющих частей с параллельной модернизацией.',
    'long_description': '# Rocshelf\n\nrocshelf - препроцессор для компиляции веб-страниц из составляющих частей с параллельной модернизацией.\nЗа основу взята идея максимального разделение кода на независимые части, которые сливаются в единое целое при компиляции.\n',
    'author': 'rocshers',
    'author_email': 'prog.rocshers@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rocshers/rocshelf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
