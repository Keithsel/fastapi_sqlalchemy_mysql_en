#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import Field, EmailStr, ConfigDict, HttpUrl

from backend.common.schema import SchemaBase, CustomPhoneNumber


class AuthSchemaBase(SchemaBase):
    username: str = Field(description='Username')
    password: str = Field(description='Password')


class AuthLoginParam(AuthSchemaBase):
    captcha: str = Field(description='Captcha')


class RegisterUserParam(AuthSchemaBase):
    email: EmailStr = Field(examples=['user@example.com'], description='Email')


class UpdateUserParam(SchemaBase):
    username: str = Field(description='Username')
    email: EmailStr = Field(examples=['user@example.com'], description='Email')
    phone: CustomPhoneNumber | None = Field(None, description='Phone number')


class AvatarParam(SchemaBase):
    url: HttpUrl = Field(..., description='Avatar HTTP URL')


class GetUserInfoDetail(UpdateUserParam):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='User ID')
    uuid: str = Field(description='User UUID')
    avatar: str | None = Field(None, description='Avatar')
    status: int = Field(description='Status')
    is_superuser: bool = Field(description='Is superuser')
    join_time: datetime = Field(description='Join time')
    last_login_time: datetime | None = Field(None, description='Last login time')


class ResetPassword(SchemaBase):
    username: str = Field(description='Username')
    old_password: str = Field(description='Old password')
    new_password: str = Field(description='New password')
    confirm_password: str = Field(description='Confirm password')
