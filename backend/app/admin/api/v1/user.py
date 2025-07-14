#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Query

from backend.common.security.jwt import CurrentUser, DependsJwtAuth
from backend.common.pagination import paging_data, DependsPagination, PageData
from backend.common.response.response_schema import response_base, ResponseModel, ResponseSchemaModel
from backend.database.db import CurrentSession
from backend.app.admin.schema.user import (
    RegisterUserParam,
    GetUserInfoDetail,
    ResetPassword,
    UpdateUserParam,
    AvatarParam,
)
from backend.app.admin.service.user_service import UserService

router = APIRouter()


@router.post('/register', summary='User registration')
async def user_register(obj: RegisterUserParam) -> ResponseModel:
    await UserService.register(obj=obj)
    return response_base.success()


@router.post('/password/reset', summary='Password reset', dependencies=[DependsJwtAuth])
async def password_reset(obj: ResetPassword) -> ResponseModel:
    count = await UserService.pwd_reset(obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.get('/{username}', summary='View user info', dependencies=[DependsJwtAuth])
async def get_user(username: str) -> ResponseSchemaModel[GetUserInfoDetail]:
    data = await UserService.get_userinfo(username=username)
    return response_base.success(data=data)


@router.put('/{username}', summary='Update user info', dependencies=[DependsJwtAuth])
async def update_userinfo(username: str, obj: UpdateUserParam) -> ResponseModel:
    count = await UserService.update(username=username, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put('/{username}/avatar', summary='Update avatar', dependencies=[DependsJwtAuth])
async def update_avatar(username: str, avatar: AvatarParam) -> ResponseModel:
    count = await UserService.update_avatar(username=username, avatar=avatar)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.get(
    '',
    summary=' (Fuzzy search) Paginated retrieval of all users',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_all_users(
    db: CurrentSession,
    username: Annotated[str | None, Query()] = None,
    phone: Annotated[str | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
) -> ResponseSchemaModel[PageData[GetUserInfoDetail]]:
    user_select = await UserService.get_select(username=username, phone=phone, status=status)
    page_data = await paging_data(db, user_select)
    return response_base.success(data=page_data)


@router.delete(
    path='/{username}',
    summary='User deletion',
    description='User deletion != user logout, after deletion the user will be removed from the database',
    dependencies=[DependsJwtAuth],
)
async def delete_user(current_user: CurrentUser, username: str) -> ResponseModel:
    count = await UserService.delete(current_user=current_user, username=username)
    if count > 0:
        return response_base.success()
    return response_base.fail()
