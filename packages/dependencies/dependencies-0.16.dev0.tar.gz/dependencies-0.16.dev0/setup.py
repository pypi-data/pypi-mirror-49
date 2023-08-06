# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['dependencies', 'dependencies._checks', 'dependencies.contrib']

package_data = \
{'': ['*']}

extras_require = \
{'mkdocs': ['mkdocs', 'mkdocs-material']}

setup_kwargs = {
    'name': 'dependencies',
    'version': '0.16.dev0',
    'description': 'Dependency Injection for Humans',
    'long_description': '![logo](https://raw.githubusercontent.com/dry-python/brand/master/logo/dependencies.png)\n\n[![azure-pipeline](https://dev.azure.com/dry-python/dependencies/_apis/build/status/dry-python.dependencies?branchName=master)](https://dev.azure.com/dry-python/dependencies/_build/latest?definitionId=2&branchName=master)\n[![codecov](https://codecov.io/gh/dry-python/dependencies/branch/master/graph/badge.svg)](https://codecov.io/gh/dry-python/dependencies)\n[![docs](https://readthedocs.org/projects/dependencies/badge/?version=latest)](https://dependencies.readthedocs.io/en/latest/?badge=latest)\n[![gitter](https://badges.gitter.im/dry-python/dependencies.svg)](https://gitter.im/dry-python/dependencies)\n[![pypi](https://img.shields.io/pypi/v/dependencies.svg)](https://pypi.python.org/pypi/dependencies/)\n[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n-----\n\n# Dependency Injection for Humans\n\n* [Source Code](https://github.com/dry-python/dependencies)\n* [Issue Tracker](https://github.com/dry-python/dependencies/issues)\n* [Documentation](https://dependencies.readthedocs.io/en/latest/)\n* [Discussion](https://gitter.im/dry-python/dependencies)\n\n## Installation\n\nAll released versions are hosted on the Python Package Index. You can\ninstall this package with following command.\n\n```bash\npip install dependencies\n```\n\n## Usage\n\nDependency injection without `dependencies`\n\n```python\nrobot = Robot(\n    servo=Servo(amplifier=Amplifier()),\n    controller=Controller(),\n    settings=Settings(environment="production"),\n)\n\nrobot.work()\n```\n\nDependency injection with `dependencies`\n\n```python\nclass Container(Injector):\n    robot = Robot\n    servo = Servo\n    amplifier = Amplifier\n    controller = Controller\n    settings = Settings\n    environment = "production"\n\nContainer.robot.work()\n```\n\n## License\n\nDependencies library is offered under the two clause BSD license.\n',
    'author': 'Artem Malyshev',
    'author_email': 'proofit404@gmail.com',
    'url': 'https://dry-python.org/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
