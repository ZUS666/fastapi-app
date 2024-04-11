import uuid

import bcrypt

from adapters.broker.notify_base import INotifyService
from core.dependency import impl
from domain.constants.user_constants import LEN_CONFIRMATION_CODE
from domain.custom_types.types_users import UIDType
from domain.exceptions.user_exceptions import (
    InvalidActivationCodeError,
    InvalidPasswordError,
    UserAlreadyActivatedError,
    UserAlreadyExistError,
    UserNotActivatedError,
    UserNotFoundError,
)
from domain.schemas.auth_schemas import TokenResponseSchema
from domain.schemas.user_schemas import (
    ActivationUserSchema,
    ProfileSchema,
    ProfileUpdateSchema,
    ResendActivationSchema,
    SuccessResponse,
    UserCredentialsSchema,
    UserInfoSchema,
    UserLoginSchema,
    UserRegistrationInputSchema,
)
from domain.services.auth_service import JWTService
from domain.services.notify_service import CreateNotifySendSchema
from repositories.cache.base_cache import IUserCodeCache
from repositories.repository import IUserRepository


class HashService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password."""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(password_bytes, salt)
        return hash.decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify password."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


class ActivationCodeService:
    def __init__(self):
        self.cache: IUserCodeCache = impl.container.resolve(IUserCodeCache)

    @staticmethod
    def _get_random_code() -> str:
        """Creates a random confirmation code."""
        return str(uuid.uuid4().int)[:LEN_CONFIRMATION_CODE]

    async def create_code(self, user_id: UIDType) -> str:
        code = self._get_random_code()
        await self.cache.set(str(user_id), code)
        return code

    async def verify_code(self, user_id: UIDType, code: str) -> bool:
        cached_code = await self.cache.get(str(user_id))
        return code == cached_code


class UserService:
    def __init__(
        self,
    ) -> None:
        self.repository: IUserRepository = impl.container.resolve(IUserRepository)

    async def create(self, user: UserRegistrationInputSchema) -> UserInfoSchema:
        """Create new user in database."""
        user.password = HashService.hash_password(user.password)
        user_schema = await self.repository.create(user)
        if not user_schema:
            raise UserAlreadyExistError
        await self._create_code_activation_notify_user(user_schema)
        return user_schema

    async def login(
        self,
        user_login: UserLoginSchema,
    ) -> TokenResponseSchema:
        """Login user returning tokens."""
        user: UserCredentialsSchema | None = await self.repository.get_by_email(user_login.email)
        if not user:
            raise UserNotFoundError
        if not user.is_active:
            raise UserNotActivatedError
        if not HashService.verify_password(user_login.password, user.password):
            raise InvalidPasswordError
        return JWTService.create_tokens(user.user_id)

    async def get_user_info_by_id(self, user_id: UIDType) -> UserInfoSchema:
        """Get user info."""
        user_schema = await self.repository.get_user_info_by_id(user_id)
        if not user_schema:
            raise UserNotFoundError
        return user_schema

    async def update_profile(
        self, user_id: UIDType, profile: ProfileUpdateSchema
    ) -> ProfileSchema:
        """Update profile."""
        schema = await self.repository.update_profile(user_id, profile)
        if not schema:
            raise UserNotFoundError
        return schema

    async def resend_activation(self, email: ResendActivationSchema) -> SuccessResponse:
        """Resend activation."""
        user = await self.repository.get_user_info_by_email(email.email)
        if not user:
            raise UserNotFoundError
        if user.is_active:
            raise UserAlreadyActivatedError
        await self._create_code_activation_notify_user(user)
        return SuccessResponse(success=True)

    async def activate_user(self, schema: ActivationUserSchema) -> SuccessResponse:
        """Activate user."""
        user = await self.repository.get_by_email(schema.email)
        if not user:
            raise UserNotFoundError
        if user.is_active:
            raise UserAlreadyActivatedError
        code = await ActivationCodeService().verify_code(user.user_id, schema.code)
        if not code:
            raise InvalidActivationCodeError
        await self.repository.activate_user(user.user_id)
        return SuccessResponse(success=True)

    @staticmethod
    async def _create_code_activation_notify_user(user_schema: UserInfoSchema) -> None:
        code = await ActivationCodeService().create_code(user_schema.user_id)
        notify_schema = CreateNotifySendSchema.activation_code(user_schema, code)
        notify_service: INotifyService = impl.container.resolve(INotifyService)
        await notify_service.notify(notify_schema)
