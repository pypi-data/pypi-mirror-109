# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['traductorkq']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'translate>=3.5.0,<4.0.0']

setup_kwargs = {
    'name': 'traductorkq',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Traductor\n\nPrograma para traducir palabras de Ingles a Espanol\n\n## Instalacion\n\npip install traductorkq\n\n## Forma de uso\n\ntraductorkq "hello"\n\nhello -> hola',
    'author': 'Kevin',
    'author_email': 'kevin.kjqm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kevinq181/translatorkq.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
