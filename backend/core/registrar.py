#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi_limiter import FastAPILimiter
from fastapi_pagination import add_pagination

from backend.app.router import route
from backend.common.exception.exception_handler import register_exception
from backend.common.log import setup_logging, set_custom_logfile
from backend.core.path_conf import STATIC_DIR
from backend.database.redis import redis_client
from backend.core.conf import settings
from backend.database.db import create_table
from backend.utils.demo_site import demo_site
from backend.utils.health_check import http_limit_callback, ensure_unique_route_names
from backend.utils.openapi import simplify_operation_ids


@asynccontextmanager
async def register_init(app: FastAPI):
    """
    Startup initialization

    :return:
    """
    # Create database tables
    await create_table()
    # Connect to redis
    await redis_client.open()
    # Initialize limiter
    await FastAPILimiter.init(
        redis_client,
        prefix=settings.REQUEST_LIMITER_REDIS_PREFIX,
        http_callback=http_limit_callback,
    )

    yield

    # Close redis connection
    await redis_client.close()
    # Close limiter
    await FastAPILimiter.close()


def register_app():
    # FastAPI
    app = FastAPI(
        title=settings.FASTAPI_TITLE,
        version=settings.FASTAPI_VERSION,
        description=settings.FASTAPI_DESCRIPTION,
        docs_url=settings.FASTAPI_DOCS_URL,
        redoc_url=settings.FASTAPI_REDOC_URL,
        openapi_url=settings.FASTAPI_OPENAPI_URL,
        lifespan=register_init,
    )

    # Register components
    register_logger()
    register_static_file(app)
    register_middleware(app)
    register_router(app)
    register_page(app)
    register_exception(app)

    return app


def register_logger() -> None:
    """
    System logging

    :return:
    """
    setup_logging()
    set_custom_logfile()


def register_static_file(app: FastAPI):
    """
    Static file interaction in development mode, will be automatically disabled in production.
    In production, you must use nginx for static resource service.

    :param app:
    :return:
    """
    if settings.FASTAPI_STATIC_FILES:
        from fastapi.staticfiles import StaticFiles

        if not os.path.exists(STATIC_DIR):
            os.makedirs(STATIC_DIR)

        app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')


def register_middleware(app) -> None:
    # API access logging
    if settings.MIDDLEWARE_ACCESS:
        from backend.middleware.access_middle import AccessMiddleware

        app.add_middleware(AccessMiddleware)
    # CORS
    if settings.MIDDLEWARE_CORS:
        from starlette.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )


def register_router(app: FastAPI):
    """
    Router

    :param app: FastAPI
    :return:
    """
    dependencies = [Depends(demo_site)] if settings.DEMO_MODE else None

    # API
    app.include_router(route, dependencies=dependencies)

    # Extra
    ensure_unique_route_names(app)
    simplify_operation_ids(app)


def register_page(app: FastAPI):
    """
    Pagination query

    :param app:
    :return:
    """
    add_pagination(app)
