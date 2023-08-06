# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['time_robust_forest']

package_data = \
{'': ['*']}

install_requires = \
['rich>=9.8.2,<10.0.0', 'typer[all]>=0.3.2,<0.4.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.0,<2.0.0']}

entry_points = \
{'console_scripts': ['time-robust-forest = time_robust_forest.__main__:app']}

setup_kwargs = {
    'name': 'time-robust-forest',
    'version': '0.1.0',
    'description': 'Explores time information to train a robust random forest',
    'long_description': '# time-robust-forest\n\n<div align="center">\n\n[![Build status](https://github.com/lgmoneda/time-robust-forest/workflows/build/badge.svg?branch=main&event=push)](https://github.com/lgmoneda/time-robust-forest/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/time-robust-forest.svg)](https://pypi.org/project/time-robust-forest/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/lgmoneda/time-robust-forest/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/lgmoneda/time-robust-forest/blob/main/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/lgmoneda/time-robust-forest/releases)\n[![License](https://img.shields.io/github/license/lgmoneda/time-robust-forest)](https://github.com/lgmoneda/time-robust-forest/blob/main/LICENSE)\n\n</div>\n\nA Proof of concept model that explores timestamp information to train a random forest with better Out of Distribution generalization power.\n\n## Installation\n\n```bash\npip install -U time-robust-forest\n```\n\n## License\n\n[![License](https://img.shields.io/github/license/lgmoneda/time-robust-forest)](https://github.com/lgmoneda/time-robust-forest/blob/main/LICENSE)\n\nThis project is licensed under the terms of the `BSD-3` license. See [LICENSE](https://github.com/lgmoneda/time-robust-forest/blob/main/LICENSE) for more details.\n\n## 📃 Citation\n\n```\n@misc{time-robust-forest,\n  author = {Moneda, Luis},\n  title = {Time Robust Forest model},\n  year = {2021},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/lgmoneda/time-robust-forest}}\n}\n```\n',
    'author': 'lgmoneda',
    'author_email': 'lgmoneda@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lgmoneda/time-robust-forest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
