# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blacksheep_prometheus']

package_data = \
{'': ['*']}

install_requires = \
['blacksheep>=1.0.7', 'prometheus-client>=0.11.0']

setup_kwargs = {
    'name': 'blacksheep-prometheus',
    'version': '0.1.1',
    'description': 'Prometheus integration for blacksheep',
    'long_description': "# Blacksheep Prometheus\n\n[![Build Status](https://github.com/Cdayz/blacksheep-prometheus/workflows/Continuous%20Integration/badge.svg)](https://github.com/Cdayz/blacksheep-prometheus/actions)[![codecov](https://codecov.io/gh/Cdayz/blacksheep-prometheus/branch/master/graph/badge.svg?token=YJTGKBTQSE)](https://codecov.io/gh/Cdayz/blacksheep-prometheus)\n\n## Introduction\n\nPrometheus integration for Blacksheep.\n\n## Requirements\n\n* Python 3.6+\n* Blacksheep 1.0.7+\n\n## Installation\n\n```console\n$ pip install blacksheep-prometheus\n```\n\n## Usage\n\nA complete example that exposes prometheus metrics endpoint under `/metrics/` path.\n\n```python\nfrom blacksheep.server import Application\nfrom blacksheep_prometheus import PrometheusMiddleware, metrics\n\napp = Application()\n\napp.middlewares.append(PrometheusMiddleware())\napp.router.add_get('/metrics/', metrics)\n```\n\n## Contributing\n\nThis project is absolutely open to contributions so if you have a nice idea, create an issue to let the community \ndiscuss it.\n",
    'author': 'Nikita Tomchik',
    'author_email': 'cdayz@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Cdayz/blacksheep-prometheus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
