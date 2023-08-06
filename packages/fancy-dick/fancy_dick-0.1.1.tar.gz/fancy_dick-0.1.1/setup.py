# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fancy_dick']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fancy-dick',
    'version': '0.1.1',
    'description': 'Leverage the sets filling tool!',
    'long_description': "# Testnet_001\n_regnerischerbuerger's project_\n\nПроект тестовый, но уже предлагает бесполезную функцию!\n\nНу, например, используя функцию `update_a_set` вы можете обновить множество Python. \nБудто бы нам обычного метода не хватало... Ну, зато множество ошибок может быть исключено...",
    'author': 'Ruslan Nikitin',
    'author_email': 'basilstansfield@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/regnerischerbuerger/testnet_001',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
