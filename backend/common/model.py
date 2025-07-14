#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, declared_attr, mapped_column

from backend.utils.timezone import timezone

# Common Mapped type primary key, needs to be added manually, usage example below:
# MappedBase -> id: Mapped[id_key]
# DataClassBase && Base -> id: Mapped[id_key] = mapped_column(init=False)
id_key = Annotated[
    int, mapped_column(primary_key=True, index=True, autoincrement=True, sort_order=-999, comment='Primary key id')
]


# Mixin: An object-oriented programming concept to make structures clearer, see `Wiki <https://en.wikipedia.org/wiki/Mixin/>`__
class UserMixin(MappedAsDataclass):
    """User Mixin dataclass"""

    created_by: Mapped[int] = mapped_column(sort_order=998, comment='Creator')
    updated_by: Mapped[int | None] = mapped_column(init=False, default=None, sort_order=998, comment='Updater')


class DateTimeMixin(MappedAsDataclass):
    """Datetime Mixin dataclass"""

    created_time: Mapped[datetime] = mapped_column(
        init=False, default_factory=timezone.now, sort_order=999, comment='Creation time'
    )
    updated_time: Mapped[datetime | None] = mapped_column(
        init=False, onupdate=timezone.now, sort_order=999, comment='Update time'
    )


class MappedBase(AsyncAttrs, DeclarativeBase):
    """
    Declarative base class, serves as the parent class for all base or data model classes

    `AsyncAttrs <https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncAttrs>`__
    `DeclarativeBase <https://docs.sqlalchemy.org/en/20/orm/declarative_config.html>`__
    `mapped_column() <https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column>`__
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class DataClassBase(MappedAsDataclass, MappedBase):
    """
    Declarative dataclass base, integrates dataclass features, allows for more advanced configuration,
    but you must pay attention to some of its characteristics, especially when used with DeclarativeBase

    `MappedAsDataclass <https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses>`__
    """  # noqa: E501

    __abstract__ = True


class Base(DataClassBase, DateTimeMixin):
    """
    Declarative Mixin dataclass base, integrates dataclass features and includes Mixin dataclass base table structure.
    You can simply think of it as a dataclass base with basic table structure.
    """  # noqa: E501

    __abstract__ = True

