#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import ExpiredSignatureError, JWTError, jwt
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

from backend.app.admin.model import User
from backend.common.exception.errors import AuthorizationError, TokenError
from backend.core.conf import settings
from backend.database.db import CurrentSession

oauth2_schema = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL_SWAGGER)

password_hash = PasswordHash((BcryptHasher(),))


def get_hash_password(password: str, salt: bytes | None) -> str:
    """
    Encrypt passwords using the hash algorithm

    :param password:
    :param salt:
    :return:
    """
    return password_hash.hash(password, salt=salt)


def password_verify(plain_password: str, hashed_password: str) -> bool:
    """
    Password verification

    :param plain_password: The password to verify
    :param hashed_password: The hash ciphers to compare
    :return:
    """
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(sub: str) -> str:
    """
    Generate encrypted token

    :param sub: The subject/userid of the JWT
    :return:
    """
    to_encode = {'sub': sub}
    access_token = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)
    return access_token


def get_token(request: Request) -> str:
    """
    Get token from request header

    :return:
    """
    authorization = request.headers.get('Authorization')
    scheme, token = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != 'bearer':
        raise TokenError(msg='Invalid token')
    return token


def jwt_decode(token: str) -> int:
    """
    Decode token

    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        user_id = int(payload.get('sub'))
        if not user_id:
            raise TokenError(msg='Invalid token')
    except ExpiredSignatureError:
        raise TokenError(msg='Token expired')
    except (JWTError, Exception):
        raise TokenError(msg='Invalid token')
    return user_id


async def get_current_user(db: CurrentSession, token: str = Depends(oauth2_schema)) -> User:
    """
    Get current user by token

    :param db:
    :param token:
    :return:
    """
    user_id = jwt_decode(token)
    from backend.app.admin.crud.crud_user import user_dao

    user = await user_dao.get(db, user_id)
    if not user:
        raise TokenError(msg='Invalid token')
    if not user.status:
        raise AuthorizationError(msg='User has been locked, please contact the system administrator')
    return user


def superuser_verify(user: User):
    """
    Verify if the current user is a superuser

    :param user:
    :return:
    """
    superuser = user.is_superuser
    if not superuser:
        raise AuthorizationError
    return superuser


# User dependency injection
CurrentUser = Annotated[User, Depends(get_current_user)]
# Permission dependency injection
DependsJwtAuth = Depends(get_current_user)
