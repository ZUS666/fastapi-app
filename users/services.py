import datetime as dt
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from jose import jwt
from jose.exceptions import JWTError
from core.settings import settings
from core.core_types import UIDType

from users.constants import ExceptionMessage, TokenEnum
from users.repository import UserRepository
from users.schemas import (
    AccessTokenSchema,
    ProfileSchema,
    RefreshTokenSchema,
    TokenResponseSchema,
    UserInfoSchema,
    UserLoginSchema,
    UserQueriesSchema,
    UserRegistrationResponseSchema,
    UserRegistrationSchema,
    UserSchema,
)


class HashService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password."""
        return CryptContext(schemes=['bcrypt']).hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify password."""
        return CryptContext(schemes=['bcrypt']).verify(password, hashed_password)


class JWTService:
    @staticmethod
    def _create_token(user_id: UIDType, expires_in: TokenEnum, token_type: TokenEnum) -> str:
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
    def get_user_id_from_access_token(cls, token: str) -> int:
        """Get user id from token."""
        return cls._get_user_id_from_token(token, TokenEnum.access)

    @classmethod
    def _get_user_id_from_refresh_token(cls, token: str) -> int:
        """Get user id from token."""
        return cls._get_user_id_from_token(token, TokenEnum.refresh)

    @staticmethod
    def _get_user_id_from_token(token: str, expected_type: TokenEnum) -> int:
        """Get user id from token."""
        invalid_token_error = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ExceptionMessage.INVALID_TOKEN,
        )
        try:
            payload: dict[str, str | int] = jwt.decode(
                token=token,
                key=settings.token.secret_key,
                algorithms=TokenEnum.ALGORITHM.value,
            )
            user_id = payload.get('user_id')
            if (
                payload.get('token_type') == expected_type.value and
                isinstance(user_id, UIDType)
            ):
                return user_id
            raise invalid_token_error
        except JWTError:
            raise invalid_token_error

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
    def create_access_token_from_refresh(cls, token: str) -> AccessTokenSchema:
        """Create access token."""
        instance = cls()
        user_id = instance._get_user_id_from_token(token, TokenEnum.refresh)
        return instance._create_access_token(user_id)


class PermissionService:
    @staticmethod
    async def get_current_user_id(
        token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    ) -> int:
        return JWTService.get_user_id_from_access_token(token.credentials)

class UserService:
    def __init__(
        self, repository: Annotated[UserRepository, Depends(UserRepository)]
    ) -> None:
        self.repository = repository

    async def get(self, quieris: UserQueriesSchema) -> list[UserSchema | None]:
        """Get collection of users from database."""
        users = await self.repository.list(quieris)
        return [UserSchema.model_validate(user) for user in users]

    async def get_by_id(self, user_id: UIDType) -> UserSchema | None:
        """Get user by id from database."""
        user = await self.repository.get_by_id(user_id)
        if user:
            return UserSchema.model_validate(user)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ExceptionMessage.USER_NOT_FOUND,
        )

    async def create(
        self,
        user: UserRegistrationSchema
    ) -> UserRegistrationResponseSchema:
        """Create new user in database."""
        user_exists = await self.repository.exists_by_email(user.email)
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ExceptionMessage.USER_ALREADY_EXISTS,
            )
        user.password = HashService.hash_password(user.password)
        user_model = await self.repository.create(user)
        return UserRegistrationResponseSchema.model_validate(user_model)

    async def login(
        self,
        user_login: UserLoginSchema,
    ) -> TokenResponseSchema:
        """Login user."""
        user = await self.repository.get_by_email(user_login.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ExceptionMessage.USER_NOT_FOUND,
            )
        if not HashService.verify_password(user_login.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ExceptionMessage.INVALID_PASSWORD,
            )
        return JWTService.create_tokens(user.user_id)
    
    async def get_user_info(
        self,
        user_id: UIDType
    ) -> UserInfoSchema:
        """Get user info."""
        user = await self.repository.get_user_info_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ExceptionMessage.USER_NOT_FOUND,
            )
        return UserInfoSchema.model_validate(user)
        # return UserInfoSchema(
        #     user_id=user.user_id,
        #     email=user.email,
        #     profile=ProfileSchema(
        #         first_name=user.profile.first_name,
        #         last_name=user.profile.last_name
        #     ),
        # )
