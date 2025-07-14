#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import String, VARBINARY
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import DataClassBase, id_key
from backend.database.db import uuid4_str
from backend.utils.timezone import timezone


class User(DataClassBase):
    """User table"""

    __tablename__ = 'sys_user'

    id: Mapped[id_key] = mapped_column(init=False)
    uuid: Mapped[str] = mapped_column(String(50), init=False, default_factory=uuid4_str, unique=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True, comment='Username')
    password: Mapped[str] = mapped_column(String(255), comment='Password')
    salt: Mapped[bytes | None] = mapped_column(VARBINARY(255), comment='Encryption salt')
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True, comment='Email')
    status: Mapped[int] = mapped_column(default=1, comment='User account status (0 disabled, 1 active)')
    is_superuser: Mapped[bool] = mapped_column(default=False, comment='Superuser privilege (0 no, 1 yes)')
    avatar: Mapped[str | None] = mapped_column(String(255), default=None, comment='Avatar')
    phone: Mapped[str | None] = mapped_column(String(11), default=None, comment='Phone number')
    join_time: Mapped[datetime] = mapped_column(init=False, default_factory=timezone.now, comment='Registration time')
    last_login_time: Mapped[datetime | None] = mapped_column(init=False, onupdate=timezone.now, comment='Last login')
