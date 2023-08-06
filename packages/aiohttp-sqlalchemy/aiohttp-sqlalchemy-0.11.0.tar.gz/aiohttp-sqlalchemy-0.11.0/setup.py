# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiohttp_sqlalchemy']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.17,<2.0.0', 'aiohttp>=3.7.4.post0,<4.0.0']

setup_kwargs = {
    'name': 'aiohttp-sqlalchemy',
    'version': '0.11.0',
    'description': 'SQLAlchemy 1.4 / 2.0 support for aiohttp.',
    'long_description': "==================\naiohttp-sqlalchemy\n==================\n.. image:: https://readthedocs.org/projects/aiohttp-sqlalchemy/badge/?version=latest\n  :target: https://aiohttp-sqlalchemy.readthedocs.io/en/latest/?badge=latest\n  :alt: Documentation Status\n\n.. image:: https://badge.fury.io/py/aiohttp-sqlalchemy.svg\n  :target: https://badge.fury.io/py/aiohttp-sqlalchemy\n\n.. image:: https://img.shields.io/pypi/dm/aiohttp-sqlalchemy\n  :target: https://pypistats.org/packages/aiohttp-sqlalchemy\n  :alt: Downloads count\n\n.. image:: https://travis-ci.com/ri-gilfanov/aiohttp-sqlalchemy.svg?branch=master\n  :target: https://travis-ci.com/ri-gilfanov/aiohttp-sqlalchemy\n\n.. image:: https://coveralls.io/repos/github/ri-gilfanov/aiohttp-sqlalchemy/badge.svg?branch=master\n  :target: https://coveralls.io/github/ri-gilfanov/aiohttp-sqlalchemy?branch=master\n\nSQLAlchemy 1.4 / 2.0 support for aiohttp.\n\nThe library provides the next features:\n\n* initializing asynchronous sessions through a middlewares;\n* initializing asynchronous sessions through a decorators;\n* simple access to one asynchronous session by default key;\n* support for different types of request handlers.\n\n\nDocumentation\n-------------\nhttps://aiohttp-sqlalchemy.readthedocs.io\n\n\nInstallation\n------------\n::\n\n    pip install aiohttp-sqlalchemy\n\n\nSimple example\n--------------\nInstall ``aiosqlite`` for work with sqlite3: ::\n\n  pip install aiosqlite\n\nCopy and paste this code in a file and run:\n\n.. code-block:: python\n\n  from aiohttp import web\n  import aiohttp_sqlalchemy\n  from aiohttp_sqlalchemy import sa_bind, sa_session\n  from datetime import datetime\n  import sqlalchemy as sa\n  from sqlalchemy import orm\n  from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine\n\n\n  metadata = sa.MetaData()\n  Base = orm.declarative_base(metadata=metadata)\n\n\n  class MyModel(Base):\n      __tablename__ = 'my_table'\n      id = sa.Column(sa.Integer, primary_key=True)\n      timestamp = sa.Column(sa.DateTime(), default=datetime.now)\n\n\n  async def main(request):\n      async with sa_session(request).bind.begin() as conn:\n          await conn.run_sync(Base.metadata.create_all)\n\n      async with sa_session(request).begin():\n          sa_session(request).add_all([MyModel()])\n          result = await sa_session(request).execute(sa.select(MyModel))\n          data = {r.id: r.timestamp.isoformat() for r in result.scalars()}\n          return web.json_response(data)\n\n\n  app = web.Application()\n\n  engine = create_async_engine('sqlite+aiosqlite:///')\n  Session = orm.sessionmaker(engine, AsyncSession)\n  aiohttp_sqlalchemy.setup(app, [sa_bind(Session)])\n\n  app.add_routes([web.get('/', main)])\n\n  if __name__ == '__main__':\n      web.run_app(app)\n",
    'author': 'Ruslan Ilyasovich Gilfanov',
    'author_email': 'ri.gilfanov@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ri-gilfanov/aiohttp-sqlalchemy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
