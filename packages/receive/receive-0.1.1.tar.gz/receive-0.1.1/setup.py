# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['receive']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'receive',
    'version': '0.1.1',
    'description': 'Host a temporary HTTP server to receive a web-hook callback.',
    'long_description': '# Receive\n\n`receive` is a python library for hosting temporary web servers and receiving values from their route handlers via futures. \n\n## Install\n\n### Stable Release\n\n```\npip install receive\n```\n\n### Latest Features\n\n```\npip install git+https://github.com/BlakeASmith/receive\n```\n\n## Usage\n\n### Handle a GET request\n\nFirst, define a route handler as follows:\n```python\nimport receive\n\n@receive.get_request(route="/callback", port=5000)\nasync def get_query_param_from_request(req):\n    return req.query["code"]\n```\n\nThe `req` parameter is an [aiohttp.web.Request](https://docs.aiohttp.org/en/stable/web_reference.html) object. In this example\nwe return the `code` query parameter from the request. \n\nNow we can start a temporary web server, and get our return value from the first request that comes in.\n\n```python\nimport asyncio\n\nasync def main():\n    future = await get_query_param_from_request()\n    code = await future\n    print(code)\n    \n    \nif __name__ == "__main__":\n    asyncio.get_event_loop().run_until_complete(main)\n```\n\nThe `get_query_param_from_request` function will start a web server in the background and return a `asyncio.Future` object providing access to the \nreturn value from the handler. `get_query_param_from_request` will return immediately, and invoking\n`await` on the returned future will block until a `GET 0.0.0.0:5000/callback` request hits the server. At that time the future will be completed with the \nvalue returned from the request handler and the \nserver will be shutdown.\n\n\n## Tests\n\nRun the unit tests using pytest\n\n```\npoetry install\npoetry run pytest\n```\n',
    'author': 'Blake Smith',
    'author_email': 'blakeinvictoria@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
