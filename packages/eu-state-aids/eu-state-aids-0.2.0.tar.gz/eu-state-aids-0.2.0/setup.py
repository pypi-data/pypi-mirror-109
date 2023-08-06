# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eu_state_aids']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=4.5.0,<5.0.0',
 'openpyxl>=3.0.7,<4.0.0',
 'pandas>=1.2.4,<2.0.0',
 'requests-mock>=1.9.3,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'typer>=0.3.2,<0.4.0',
 'validators>=0.18.2,<0.19.0']

entry_points = \
{'console_scripts': ['eu-state-aids = eu_state_aids.main:app']}

setup_kwargs = {
    'name': 'eu-state-aids',
    'version': '0.2.0',
    'description': 'CLI to extract state aids data from public sources and produce CSV files',
    'long_description': '## Description\n\n`eu-state-aids` is a Command Line Interface that can be used \nto import **state aids related data** from single countries sources sitesm\nand produce CSV files, according to a common  data structure.\n\n\n![TravisCI Badge](https://travis-ci.com/openpolis/eu-state-aids.svg?branch=master "TravisCI building status")\n[![PyPI version](https://badge.fury.io/py/eu-state-aids.svg)](https://badge.fury.io/py/eu-state-aids)\n![Tests Badge](https://op-badges.s3.eu-west-1.amazonaws.com/eu-state-aids/tests-badge.svg)\n![Coverage Badge](https://op-badges.s3.eu-west-1.amazonaws.com/eu-state-aids/coverage-badge.svg)\n\n## Installation\n\nPython versions from 3.7 are supported.\n \nThe package depends on these python packages:\n* typer\n* openpyxl\n* pandas\n* requests\n* validators\n\nSo, it\'s better to create a *virtualenv* before installation.\n\nThe package is hosted on pypi, and can be installed, for example using pip:\n\n    pip install eu-state-aids \n\n\n## Usage\n\nThe `eu-state-aids` binary command will be available after installation. \nIt offers help with:\n\n    eu-state-aids --help\n\nThe `opstate-aids` command can be used to extract the data from the official sources, \nand populate the CSV files.\n\nFor each country, data files will firstly be *fetched* and stored locally, \nand thereafter *used* in order to **export** CSV files.\n\nThis two-step procedure is useful, since it is not always possible to download source files (Excel, XML, ...) from \nBI systems of nation states, as it has been seen that they tend to time-out whenever the number of records is \nhigh enough.\n\nThe logic of these two phases can vary for each single european state, so each country will have a dedicated module,\nthat will be executable as a sub-command.\n\nTo retrieve data and produce a CSV file for Bulgary (bg), 2015:\n \n      eu-state-aids bg fetch 2015\n      eu-state-aids bg export 2015\n\nTo launch the scripts *for all years* for Bulgary (bg):\n\n    # download all years\' excel files into local storage \n    for Y in $(seq 2014 2022)\n    do \n      eu-state-aids bg fetch $Y\n    done\n    \n    # process all years\' excel files and export CSV records into local storage \n    #./data/bg/$Y.csv files\n    for Y in $(seq 2014 2022)\n      eu-state-aids bg export $Y\n    done\n\n## Support\n\nThere is no guaranteed support available, but issues can be created on this project \nand the authors will try to answer and merge proposed solutions into the code base.\n\n## Project Status\nThis project is funded by the European Commission and is currently (2021) under active developement.\n\n## Contributing\nIn order to contribute to this project:\n* verify that python 3.7+ is being used (or use [pyenv](https://github.com/pyenv/pyenv))\n* verify or install [poetry](https://python-poetry.org/), to handle packages and dependencies in a leaner way, \n  with respect to pip and requirements\n* clone the project `git clone git@github.com:openpolis/eu-state-aids.git` \n* install the dependencies in the virtualenv, with `poetry install`,\n  this will also install the dev dependencies\n* develop wildly, running tests and coverage with `coverage run -m pytest`\n\n### Testing\nTests are under the tests folder. [requests-mock](https://requests-mock.readthedocs.io/en/latest/index.html)\nis used to mock requests to remote data files, in order to avoid slow remote connections during tests.\n\n## Authors\nGuglielmo Celata - guglielmo@openpolis.it\n\n## Licensing\nThis package is released under an MIT License, see details in the LICENSE.txt file.\n\n',
    'author': 'guglielmo',
    'author_email': 'guglielmo@openpolis.it',
    'maintainer': 'guglielmo',
    'maintainer_email': 'guglielmo@openpolis.it',
    'url': 'https://github.com/openpolis/eu-state-aids/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
