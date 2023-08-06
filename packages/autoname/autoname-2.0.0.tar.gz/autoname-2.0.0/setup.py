# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autoname']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'autoname',
    'version': '2.0.0',
    'description': 'an enum `AutoName` from python docs with multiple stringcase options',
    'long_description': '\n# autoname\n\nan enum `AutoName` from [python docs](https://docs.python.org/3/library/enum.html#using-automatic-values) with multiple stringcase options.\n\n## Get Started\n\n```bash\n$ pip install autoname\n```\n\n```python\nfrom autoname import AutoName\nfrom enum import auto\n\n\n# an enum class\nclass GameType(AutoName):\n    INDIE = auto()\n\n\nprint(GameType.INDIE.value)  # "INDIE"\n\n# could be alternative in pydantic instead of literal\nfrom pydantic import BaseModel\n\n\nclass Game(BaseModel):\n    type: GameType\n```\n\nAlso have others stringcases coverter\n1. `AutoNameLower` - convert name value to lowercase\n2. `AutoNameUpper` - convert name value to uppercase\n\ne.g.\n```python\nfrom autoname import AutoNameLower\nfrom enum import auto\n\nclass GameType(AutoNameLower):\n    INDIE = auto()\n\nprint(GameType.INDIE.value) # "indie"\n```\n\nYou could also bring your own case convertion algorithm.\n\n```python\nfrom autoname import AutoName, transform\nfrom enum import auto\n\n\n@transform(function=str.lower)\nclass GameType(AutoName):\n    INDIE = auto()\n\n\nprint(GameType.INDIE.value)  # "indie"\n```\n\nIf the `autoname` is not a sound variable name. there are alias too.\n- `StrEnum` = `AutoName`\n- `LowerStrEnum` = `AutoNameLower`\n- `UpperStrEnum` = `AutoNameUpper`\n\ne.g.\n```python\nfrom autoname import StrEnum, transform\nfrom enum import auto\n\n\nclass GameType(StrEnum):\n    INDIE = auto()\n\n\nprint(GameType.INDIE.value)  # "INDIE"\n```\n\n## Alternative \n- `StrEnum` from [`fastapi-utils`](https://github.com/dmontagu/fastapi-utils)\n',
    'author': 'Nutchanon Ninyawee',
    'author_email': 'me@nutchanon.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CircleOnCircles/autoname',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
