from abc import ABCMeta
from aiohttp.abc import AbstractView
from aiohttp.web import View
from typing import TYPE_CHECKING

from aiohttp_sqlalchemy.constants import DEFAULT_KEY

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from typing import Any


class SAAbstractView(AbstractView, metaclass=ABCMeta):
    """
    Simple SQLAlchemy view based on aiohttp.abc.AbstractView.

    The `__await__` method must be implemented in child classes.

    Suitable for a specific usage with multiple models.
    """
    def sa_session(self, key: str = DEFAULT_KEY) -> 'AsyncSession':
        return self.request[key]


class SAOneModelMixin(SAAbstractView, metaclass=ABCMeta):
    """
    One model SQLAlchemy view based on aiohttp.abc.AbstractView.

    The `__await__` method must be implemented in child classes.

    Suitable for a usually usage with one model.
    """
    sa_model: 'Any'  # Not all developers use declarative mapping


class SABaseView(View, SAAbstractView):
    """
    Simple SQLAlchemy view based on aiohttp.web.View.

    Recomended for a specific usage with multiple models.
    """


class SAView(View, SAOneModelMixin):
    """
    One model SQLAlchemy view based on aiohttp.web.View.

    Recomended for a usually usage with one model.
    """
