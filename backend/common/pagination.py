#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from math import ceil
from typing import TYPE_CHECKING, Generic, Sequence, TypeVar

from fastapi import Depends, Query
from fastapi_pagination import pagination_ctx
from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination.links.bases import create_links
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from sqlalchemy import Select
    from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')
SchemaT = TypeVar('SchemaT')


class _CustomPageParams(BaseModel, AbstractParams):
    page: int = Query(1, ge=1, description='Page number')
    size: int = Query(20, gt=0, le=100, description='Page size')  # Default 20 records

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.size,
            offset=self.size * (self.page - 1),
        )


class _Links(BaseModel):
    first: str = Field(..., description='First page link')
    last: str = Field(..., description='Last page link')
    self: str = Field(..., description='Current page link')
    next: str | None = Field(None, description='Next page link')
    prev: str | None = Field(None, description='Previous page link')


class _PageDetails(BaseModel):
    items: list = Field([], description='Current page data')
    total: int = Field(..., description='Total count')
    page: int = Field(..., description='Current page')
    size: int = Field(..., description='Items per page')
    total_pages: int = Field(..., description='Total pages')
    links: _Links


class _CustomPage(_PageDetails, AbstractPage[T], Generic[T]):
    __params_type__ = _CustomPageParams

    @classmethod
    def create(
        cls,
        items: list,
        total: int,
        params: _CustomPageParams,
    ) -> _CustomPage[T]:
        page = params.page
        size = params.size
        total_pages = ceil(total / params.size)
        links = create_links(
            first={'page': 1, 'size': size},
            last={'page': f'{ceil(total / params.size)}', 'size': size} if total > 0 else {'page': 1, 'size': size},
            next={'page': f'{page + 1}', 'size': size} if (page + 1) <= total_pages else None,
            prev={'page': f'{page - 1}', 'size': size} if (page - 1) >= 1 else None,
        ).model_dump()

        return cls(
            items=items,
            total=total,
            page=params.page,
            size=params.size,
            total_pages=total_pages,
            links=links,  # type: ignore
        )


class PageData(_PageDetails, Generic[SchemaT]):
    """
    Unified return model containing data schema, suitable for paginated APIs

    E.g. ::

        @router.get('/test', response_model=ResponseSchemaModel[PageData[GetApiDetail]])
        def test():
            return ResponseSchemaModel[PageData[GetApiDetail]](data=GetApiDetail(...))


        @router.get('/test')
        def test() -> ResponseSchemaModel[PageData[GetApiDetail]]:
            return ResponseSchemaModel[PageData[GetApiDetail]](data=GetApiDetail(...))


        @router.get('/test')
        def test() -> ResponseSchemaModel[PageData[GetApiDetail]]:
            res = CustomResponseCode.HTTP_200
            return ResponseSchemaModel[PageData[GetApiDetail]](code=res.code, msg=res.msg, data=GetApiDetail(...))
    """

    items: Sequence[SchemaT]


async def paging_data(db: AsyncSession, select: Select) -> dict:
    """
    Create paginated data based on SQLAlchemy

    :param db:
    :param select:
    :return:
    """
    paginated_data: _CustomPage = await paginate(db, select)
    page_data = paginated_data.model_dump()
    return page_data


# Pagination dependency injection
DependsPagination = Depends(pagination_ctx(_CustomPage))
