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
    'version': '0.9.2',
    'description': 'SQLAlchemy 1.4 / 2.0 support for aiohttp.',
    'long_description': "==================\naiohttp-sqlalchemy\n==================\n.. image:: https://readthedocs.org/projects/aiohttp-sqlalchemy/badge/?version=latest\n  :target: https://aiohttp-sqlalchemy.readthedocs.io/en/latest/?badge=latest\n  :alt: Documentation Status\n\n.. image:: https://badge.fury.io/py/aiohttp-sqlalchemy.svg\n  :target: https://badge.fury.io/py/aiohttp-sqlalchemy\n\n.. image:: https://img.shields.io/pypi/dm/aiohttp-sqlalchemy\n  :target: https://pypistats.org/packages/aiohttp-sqlalchemy\n  :alt: Downloads count\n\n.. image:: https://travis-ci.com/ri-gilfanov/aiohttp-sqlalchemy.svg?branch=master\n  :target: https://travis-ci.com/ri-gilfanov/aiohttp-sqlalchemy\n\n.. image:: https://coveralls.io/repos/github/ri-gilfanov/aiohttp-sqlalchemy/badge.svg?branch=master\n  :target: https://coveralls.io/github/ri-gilfanov/aiohttp-sqlalchemy?branch=master\n\nSQLAlchemy 1.4 / 2.0 support for aiohttp.\n\nLibrary forward a ``sqlalchemy.ext.asyncio.AsyncSession`` object as\n``request['sa_main']`` or ``SAView.sa_session()`` by default.\n\n\nDocumentation\n-------------\nhttps://aiohttp-sqlalchemy.readthedocs.io/\n\n\nInstallation\n------------\n::\n\n    pip install aiohttp-sqlalchemy\n\n\nSimple example\n--------------\nInstall ``aiosqlite`` for work with sqlite3: ::\n\n  pip install aiosqlite\n\nCopy and paste this code in a file and run:\n\n.. code-block:: python\n\n  from aiohttp import web\n  import aiohttp_sqlalchemy\n  from aiohttp_sqlalchemy import sa_bind\n  from datetime import datetime\n  import sqlalchemy as sa\n  from sqlalchemy import orm\n  from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine\n\n\n  metadata = sa.MetaData()\n  Base = orm.declarative_base(metadata=metadata)\n\n\n  class MyModel(Base):\n      __tablename__ = 'my_table'\n      id = sa.Column(sa.Integer, primary_key=True)\n      timestamp = sa.Column(sa.DateTime(), default=datetime.now)\n\n\n  async def main(request):\n      async with request['sa_main'].bind.begin() as conn:\n          await conn.run_sync(Base.metadata.create_all)\n\n      async with request['sa_main'].begin():\n          request['sa_main'].add_all([MyModel()])\n          result = await request['sa_main'].execute(sa.select(MyModel))\n          data = {r.id: r.timestamp.isoformat() for r in result.scalars()}\n          return web.json_response(data)\n\n\n  app = web.Application()\n\n  engine = create_async_engine('sqlite+aiosqlite:///')\n  Session = orm.sessionmaker(engine, AsyncSession)\n  aiohttp_sqlalchemy.setup(app, [sa_bind(Session)])\n\n  app.add_routes([web.get('/', main)])\n\n  if __name__ == '__main__':\n      web.run_app(app)\n",
    'author': 'Ruslan Ilyasovich Gilfanov',
    'author_email': 'ri.gilfanov@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ri-gilfanov/aiohttp-sqlalchemy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
