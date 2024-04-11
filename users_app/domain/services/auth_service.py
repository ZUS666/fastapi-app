import datetime as dt
from typing import Literal

from jose import jwt
from jose.exceptions import JWTError

from core.settings import settings
from domain.constants.auth_constants import TokenEnum
from domain.custom_types.types_users import UIDType
from domain.exceptions.auth_exceptions import InvalidTokenError
from domain.schemas.auth_schemas import (
    AccessTokenSchema,
    RefreshTokenSchema,
    TokenResponseSchema,
)


class JWTService:
    @classmethod
    def get_user_id_from_access_token(cls, token: str) -> UIDType:
        """Get user id from token."""
        return cls._get_user_id_from_token(token, TokenEnum.access)

    @classmethod
    def create_tokens(cls, user_id: UIDType) -> TokenResponseSchema:
        """Create access and refresh tokens."""
        instance = cls()
        access_token = instance._create_access_token(user_id)
        refresh_token = instance._create_refresh_token(user_id)
        return TokenResponseSchema(
            **access_token.model_dump(), **refresh_token.model_dump()
        )

    @classmethod
    def create_access_token_by_refresh(cls, token: str) -> AccessTokenSchema:
        """Create access token."""
        instance = cls()
        user_id = instance._get_user_id_from_token(token, TokenEnum.refresh)
        return instance._create_access_token(user_id)

    @staticmethod
    def _create_token(
        user_id: UIDType,
        expires_in: Literal[TokenEnum.access_token_expires] |
        Literal[TokenEnum.refresh_token_expires],
        token_type: Literal[TokenEnum.access] | Literal[TokenEnum.refresh],
    ) -> str:
        """Create token."""
        expire = dt.datetime.now() + dt.timedelta(seconds=expires_in.value)
        data_to_encode = {
            'user_id': user_id,
            'exp': expire,
            'token_type': token_type.value,
        }
        token = jwt.encode(
            claims=data_to_encode,
            key=settings.token.secret_key,
            algorithm=TokenEnum.ALGORITHM.value,
        )
        return token

    def _create_access_token(
        self,
        user_id: UIDType,
    ) -> AccessTokenSchema:
        """Create access token."""
        token = self._create_token(
            user_id, TokenEnum.access_token_expires, TokenEnum.access
        )
        return AccessTokenSchema(
            access_token=token,
            access_token_expires_in=TokenEnum.access_token_expires.value,
        )

    def _create_refresh_token(self, user_id: UIDType) -> RefreshTokenSchema:
        """Create refresh token."""
        token = self._create_token(
            user_id, TokenEnum.refresh_token_expires, TokenEnum.refresh
        )
        return RefreshTokenSchema(
            refresh_token=token,
            refresh_token_expires_in=TokenEnum.refresh_token_expires.value,
        )

    @classmethod
    def _get_user_id_from_refresh_token(cls, token: str) -> UIDType:
        """Get user id from token."""
        return cls._get_user_id_from_token(token, TokenEnum.refresh)

    @staticmethod
    def _get_user_id_from_token(token: str, expected_type: TokenEnum) -> UIDType:
        """Get user id from token."""
        try:
            payload: dict[str, str | int | UIDType] = jwt.decode(
                token=token,
                key=settings.token.secret_key,
                algorithms=TokenEnum.ALGORITHM.value,
            )
            user_id = payload.get('user_id')
            if payload.get('token_type') == expected_type.value:
                return user_id
            raise InvalidTokenError
        except JWTError:
            raise InvalidTokenError


class PermissionService:
    @staticmethod
    def get_current_user_id(
        token: str,
    ) -> UIDType:
        """Service to get current user id by Authorization header."""
        return JWTService.get_user_id_from_access_token(token)
