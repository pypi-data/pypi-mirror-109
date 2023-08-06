# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['radio_dreams']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.3,<2.0.0', 'scipy>=1.6.3,<2.0.0', 'skyfield>=1.39,<2.0']

setup_kwargs = {
    'name': 'radio-dreams',
    'version': '0.3.0',
    'description': 'Imagined Interferometers',
    'long_description': 'Radio Dreams\n============\n\n|PyPI| |GitHub| |Coverage| |ReadTheDocs| |License| |Python| |Black|\n\n-------------------------------------------------------------------\n\nA python playground to learn how interferometers work by dreaming up imaginary arrays\n\n*radio-dreams* is designed to install cleanly with a single invocation of the standard Python package tool::\n\n    $ pip install radio-dreams\n\nHere are the essential project links:\n\n* `Home page and documentation <https://radio-dreams.readthedocs.io/en/latest/>`_\n\n* `Installing radio-dreams <https://radio-dreams.readthedocs.io/en/latest/installation.html>`_\n\n* `Example dreams <https://radio-dreams.readthedocs.io/en/latest/exampledreams.html>`_\n\n* `radio-dreams package <https://pypi.org/project/radio-dreams/>`_ on the Python Package Index\n\n* `Contributing to radio-dreams <https://github.com/amanchokshi/radio-dreams/blob/master/contrib.rst>`_\n\n* `Issue tracker <https://github.com/amanchokshi/radio-dreams/issues>`_ on GitHub\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/radio-dreams.svg?color=green&logo=python&logoColor=white&label=PyPI\n    :target: https://pypi.org/project/radio-dreams/\n    :alt: PyPI - Latest Release\n\n.. |GitHub| image:: https://img.shields.io/github/workflow/status/amanchokshi/radio-dreams/Tests?color=green&logo=github&logoColor=white&label=Tests\n    :target: https://github.com/amanchokshi/radio-dreams/actions\n    :alt: GitHub Actions - Build Status\n\n.. |Coverage| image:: https://img.shields.io/codecov/c/github/amanchokshi/radio-dreams/master.svg?color=green&logo=codecov&logoColor=white&label=Coverage\n    :target: https://codecov.io/gh/amanchokshi/radio-dreams/branch/main\n    :alt: CodeCov - Coverage Status\n\n.. |ReadTheDocs| image:: https://img.shields.io/readthedocs/radio-dreams/latest?color=green&logo=Read%20The%20Docs&logoColor=white\n    :target: https://radio-dreams.readthedocs.io\n    :alt: Documentation Status\n\n.. |License| image:: https://img.shields.io/github/license/amanchokshi/radio-dreams?color=green&label-License&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAdCAYAAADLnm6HAAAACXBIWXMAAB2HAAAdhwGP5fFlAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAflJREFUSIntljFrVUEQhb95CViYCGItGLSIIIJiISadYiOIAS0stFAEK0G0DQRs8wOs7PQvqCC2kjQJaiEICoJYaZMYzCP6WWSfLs97c/deQtJ4YODu7syZs7N7l4GOUCfVj8kmu/L0ugYCM8ChZDO7IWBPzfeOCdg5qD31urqs9q1HX11Sr6nbszl1Wl3cImkdFtXpNonm1fUOidpiXZ2vErDaELimPlDHk/9ctjaX5saTz1oD1+ogb35OD4F+RXG+Ao+AoxExGxErdVWMiJWImAUmU8y3Crd+ylV5DD31fab0gzpS4/tPBbrwDd/US8CRbDwBXKxUW4ZGvmEB9ypIquZK0cj3R4B6GjiThuvJAKbSWiuU8uUVuJ99Pwae1KkuRDmfOqFuZJfluHpM/ZXGG+rhoZjaS9iGb1CBu8Dgdj6NiNcR8RZ4nuZGgDstdl/Op+5XVzK1Z7OdnMsfD/VAUwXa8vWA28BY8nkDvBwERMQLYDkN9wK3Cnbfiq8H3MiCPwEn1H3JTgKfs/WbBQJa8Y3y9/cAuJCsDj8KBLTi6wGXgYUC4gXgSoFfK77RiHinTgHngavAKeAgMAp8AV6x+Q8/i4ifTazbzVeLrd6BNtj1nvC/gEbYvVes7v2GEAUCVtl8tbrge0SMbeVQcgR1vWIT6nu/DL8BDHb5/EeYsAMAAAAASUVORK5CYII=\n    :target: https://github.com/amanchokshi/radio-dreams/blob/master/LICENSE\n    :alt: MIT License\n\n.. |Python| image:: https://img.shields.io/badge/Python-3.7%2B-3282b8?logo=python&logoColor=white\n    :target: https://pypi.org/project/radio-dreams/\n\n.. |Black| image:: https://img.shields.io/badge/Code%20Style-Black-222222.svg?logo=powershell&logoColor=white\n    :target: https://black.readthedocs.io/\n',
    'author': 'Aman Chokshi',
    'author_email': 'achokshi@student.unimelb.edu.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/amanchokshi/radio-dreams',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
