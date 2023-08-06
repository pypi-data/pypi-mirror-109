# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blacksheep_context', 'blacksheep_context.plugins']

package_data = \
{'': ['*']}

install_requires = \
['blacksheep>=1.0.7']

setup_kwargs = {
    'name': 'blacksheep-context',
    'version': '0.1.0',
    'description': 'Middleware for blacksheep that allows you to store and access the context data of a request.',
    'long_description': "# Blacksheep Context\n\n[![Build Status](https://github.com/Cdayz/blacksheep-context/workflows/Continuous%20Integration/badge.svg)](https://github.com/Cdayz/blacksheep-context/actions)\n[![codecov](https://codecov.io/gh/Cdayz/blacksheep-context/branch/master/graph/badge.svg?token=5KFIGS17S4)](https://codecov.io/gh/Cdayz/blacksheep-context)\n[![Package Version](https://img.shields.io/pypi/v/blacksheep-context?logo=PyPI&logoColor=white)](https://pypi.org/project/blacksheep-context/)\n[![PyPI Version](https://img.shields.io/pypi/pyversions/blacksheep-context?logo=Python&logoColor=white)](https://pypi.org/project/blacksheep-context/)\n\n## Introduction\n\nMiddleware for Blacksheep that allows you to store and access the context data of a request.\nCan be used with logging so logs automatically use request headers such as x-request-id or x-correlation-id.\n\n## Requirements\n\n* Python 3.7+\n* Blacksheep 1.0.7+\n\n## Installation\n\n```console\n$ pip install blacksheep-context\n```\n\n## Usage\n\nA complete example shown below.\n\n```python\nfrom blacksheep.server import Application\nfrom blacksheep.messages import Request, Response\nfrom blacksheep.server.responses import json\n\nfrom blacksheep_context import context\nfrom blacksheep_context.middleware import ContextMiddleware\nfrom blacksheep_context.plugins import BasePlugin, HeaderPlugin\n\n\nclass RequestIdPlugin(HeaderPlugin):\n    header_key = b'X-Request-Id'\n    # Every plugin must provide this attribute\n    context_key = 'request-id'\n    # Fetches only first value of header, can be False to insert all values of header into context\n    single_value_header = True\n\n    # Also allow you to add some data from context into response\n    async def enrich_response(self, response: Response) -> None:\n        response.add_header(b'X-Request-Id', context['request_id'].encode('utf-8'))\n\n\nclass MyCustomPlugin(BasePlugin):\n    context_key = 'user-data'\n\n    # You can customize fetching data from request\n    async def process_request(self, request: Request):\n        try:\n            data = await request.json()\n            return data.get('user-id')\n        except Exception:\n            return None\n\n\nctx_middleware = ContextMiddleware(plugins=[RequestIdPlugin(), MyCustomPlugin()])\n\napp_ = Application()\napp_.middlewares.append(ctx_middleware)\n\n@app_.router.post('/ctx')\ndef return_context(request):\n    assert context.exists() is True\n    return json(context.copy())\n```\n\n## Contributing\n\nThis project is absolutely open to contributions so if you have a nice idea, create an issue to let the community \ndiscuss it.\n",
    'author': 'Nikita Tomchik',
    'author_email': 'cdayz@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Cdayz/blacksheep-context',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
