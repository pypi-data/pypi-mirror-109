# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['decorateme']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'decorateme',
    'version': '0.2.1',
    'description': 'Python decorators for str/repr, equality, immutability, and more.',
    'long_description': "# Decorate-me\n\n[![Version status](https://img.shields.io/pypi/status/decorateme?label=status)](https://pypi.org/project/decorateme)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![Python version compatibility](https://img.shields.io/pypi/pyversions/decorateme?label=Python)](https://pypi.org/project/decorateme)\n[![Version on Docker Hub](https://img.shields.io/docker/v/dmyersturnbull/decorate-me?color=green&label=Docker%20Hub)](https://hub.docker.com/repository/docker/dmyersturnbull/decorate-me)\n[![Version on Github](https://img.shields.io/github/v/release/dmyersturnbull/decorate-me?include_prereleases&label=GitHub)](https://github.com/dmyersturnbull/decorate-me/releases)\n[![Version on PyPi](https://img.shields.io/pypi/v/decorateme?label=PyPi)](https://pypi.org/project/decorateme)  \n[![Build (Actions)](https://img.shields.io/github/workflow/status/dmyersturnbull/decorate-me/Build%20&%20test?label=Tests)](https://github.com/dmyersturnbull/decorate-me/actions)\n[![Documentation status](https://readthedocs.org/projects/decorate-me/badge)](https://decorate-me.readthedocs.io/en/stable)\n[![Coverage (coveralls)](https://coveralls.io/repos/github/dmyersturnbull/decorate-me/badge.svg?branch=main&service=github)](https://coveralls.io/github/dmyersturnbull/decorate-me?branch=main)\n[![Maintainability (Code Climate)](https://api.codeclimate.com/v1/badges/ce5a27b46cbe0f3c3039/maintainability)](https://codeclimate.com/github/dmyersturnbull/decorate-me/maintainability)\n[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/dmyersturnbull/decorate-me/badges/quality-score.png?b=main)](https://scrutinizer-ci.com/g/dmyersturnbull/decorate-me/?branch=main)\n\nPython decorators for str/repr, equality, immutability, and more.\n\nSave lines and document your class’s behavior at the top.\nJust `pip install decorateme` and `import decorateme`.\n\nLicensed under the [Apache License, version 2.0](https://www.apache.org/licenses/LICENSE-2.0).\n[New issues](https://github.com/dmyersturnbull/decorate-me/issues) and pull requests are welcome.\nPlease refer to the [contributing guide](https://github.com/dmyersturnbull/decorate-me/blob/master/CONTRIBUTING.md).\nGenerated with [Tyrannosaurus](https://github.com/dmyersturnbull/tyrannosaurus).\n\n\n### List of decorators\n\n**String-like methods**\n- auto_repr_str\n- auto_str\n- auto_repr\n- auto_html (for display in Jupyter)\n- auto_info (add a .info method)\n\n**Equality**\n- auto_eq\n- auto_hash\n- total_ordering  (from functools)\n\n**Make your class smart**\n- auto_obj (auto- for eq, str, and repr)\n- dataclass (from dataclasses)\n\n**Docstring-related**\n- copy_docstring\n- append_docstring\n\n**Timing**\n- takes_seconds\n- takes_seconds_named\n- auto_timeout\n\n**Allow a class to be used as a type**\n- iterable_over\n- collection_over\n- sequence_over\n- float_type\n- int_type\n\n**Overriding / inheritance**\n- final\n- overrides\n- override_recommended\n- ABC (from abc)\n- ABCMeta  (from abc)\n- abstractmethod  (from abc)\n\n\n**Mark purpose / use**\n- internal\n- external\n- reserved\n\n**Multithreading**\n- thread_safe\n- not_thread_safe\n\n**Mutability**\n- mutable\n- immutable\n\n**Code maturity**\n- status (code deprecation & immaturity warnings)\n\n**Singletons**\n- auto_singleton\n\n\nExample of `auto_obj` and `float_type`:\n```python\nimport decorateme\n@decorateme.auto_obj()\n@decorateme.float_type('weight')\nclass Uno:\n    def __init__(self, weight):\n        self.weight = weight\nprint()\nlight1, light2, heavy = Uno(3.1), Uno(3.1), Uno(12.8)\nassert light1 == light2 != heavy\nprint(light1)  # 'Duo(weight=22.3)'\nassert light1 * heavy == 39.68\n```\n",
    'author': 'Douglas Myers-Turnbull',
    'author_email': None,
    'maintainer': 'Douglas Myers-Turnbull',
    'maintainer_email': None,
    'url': 'https://github.com/dmyersturnbull/decorate-me',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
