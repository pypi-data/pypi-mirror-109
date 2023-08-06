# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pmcli']
install_requires = \
['click>=8.0.1,<9.0.0', 'cryptocode>=0.1,<0.2']

entry_points = \
{'console_scripts': ['pm = pmcli:main']}

setup_kwargs = {
    'name': 'pmcli',
    'version': '0.1.8',
    'description': 'A Command Line Interface to encrypt, decrypt and save passwords',
    'long_description': "# PMCLI\n\n## A password encrypter and decrypter\n\n## Install\n\n#### Windows\n\npip install pmcli \n\n### How to use\n\n#### Windows\nOpen powershell and type pm\n\nEncrypting \n\nOpen Powershell and type pm. \nThen type pm encrypt\nThen it will ask for a directory. \nGive the directory with the file.txt\nNote: You don't have to make a file it makes on itself\nIt will add the file with the encrypted file\n\nDecrypting\nOpen Powershell and type pm. \nThen type pm decrypt\nThen it will ask for a directory. \nGive the directory with the file.txt\nThen it will display the decrypted text\n\n\n### Softwares used\n\nVisual Studio Code - https://github.com/Microsoft/vscode\n\nPython 3.9.1\n\n",
    'author': 'Avanindra Chakraborty',
    'author_email': 'avanindra.d2.chakraborty@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AvanindraC/PMCLI',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
