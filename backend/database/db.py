#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from typing import Annotated
from uuid import uuid4

from fastapi import Depends
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncEngine

from backend.common.log import log
from backend.common.model import MappedBase
from backend.core.conf import settings


def create_async_engine_and_session(url: str | URL) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    try:
        # Database engine
        engine = create_async_engine(
            url,
            echo=settings.DATABASE_ECHO,
            echo_pool=settings.DATABASE_POOL_ECHO,
            future=True,
            # Medium concurrency
            pool_size=10,  # Low: - High: +
            max_overflow=20,  # Low: - High: +
            pool_timeout=30,  # Low: + High: -
            pool_recycle=3600,  # Low: + High: -
            pool_pre_ping=True,  # Low: False High: True
            pool_use_lifo=False,  # Low: False High: True
        )
    except Exception as e:
        log.error('❌ Database connection failed {}', e)
        sys.exit()
    else:
        db_session = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
        return engine, db_session


async def get_db():
    """Session generator"""
    async with async_db_session() as session:
        yield session


async def create_table() -> None:
    """Create database tables"""
    async with async_engine.begin() as coon:
        await coon.run_sync(MappedBase.metadata.create_all)


def uuid4_str() -> str:
    """Database engine UUID type compatibility solution"""
    return str(uuid4())


SQLALCHEMY_DATABASE_URL = (
    f'mysql+asyncmy://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:'
    f'{settings.DATABASE_PORT}/{settings.DATABASE_SCHEMA}?charset={settings.DATABASE_CHARSET}'
)

async_engine, async_db_session = create_async_engine_and_session(SQLALCHEMY_DATABASE_URL)
# Session Annotated
CurrentSession = Annotated[AsyncSession, Depends(get_db)]
