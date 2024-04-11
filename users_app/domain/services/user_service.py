import bcrypt

from core.dependency import impl
from domain.custom_types.types_users import UIDType
from domain.exceptions.user_exceptions import (
    InvalidConfirmationCodeError,
    InvalidPasswordError,
    UserAlreadyActivatedError,
    UserAlreadyExistError,
    UserNotActivatedError,
    UserNotFoundError,
)
from domain.schemas.auth_schemas import TokenResponseSchema
from domain.schemas.user_schemas import (
    ConfirmationUserSchema,
    EmailSchema,
    ProfileSchema,
    ProfileUpdateSchema,
    ResetPasswordSchema,
    SuccessResponse,
    UserCredentialsSchema,
    UserInfoSchema,
    UserLoginSchema,
    UserRegistrationInputSchema,
)
from domain.services.auth_service import JWTService
from domain.services.common_service import ConfirmationCodeService
from domain.services.notify_service import CreateCodeNotifyUserService
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
        await CreateCodeNotifyUserService().activation_notify(user_schema)
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

    async def resend_activation(self, email: EmailSchema) -> SuccessResponse:
        """Resend activation."""
        user_schema = await self.repository.get_user_info_by_email(email.email)
        if not user_schema:
            raise UserNotFoundError
        if user_schema.is_active:
            raise UserAlreadyActivatedError
        await CreateCodeNotifyUserService().activation_notify(user_schema)
        return SuccessResponse(success=True)

    async def activate_user(self, schema: ConfirmationUserSchema) -> SuccessResponse:
        """Activate user."""
        user = await self.repository.get_by_email(schema.email)
        if not user:
            raise UserNotFoundError
        if user.is_active:
            raise UserAlreadyActivatedError
        code = await ConfirmationCodeService().verify_code(user.user_id, schema.code)
        if not code:
            raise InvalidConfirmationCodeError
        await self.repository.activate_user(user.user_id)
        return SuccessResponse(success=True)

    async def reset_password_request(self, email: EmailSchema) -> SuccessResponse:
        """Reset password request."""
        user_schema = await self.repository.get_user_info_by_email(email.email)
        if not user_schema:
            raise UserNotFoundError
        await CreateCodeNotifyUserService().reset_password_notify(user_schema)
        return SuccessResponse(success=True)

    async def reset_password(self, schema: ResetPasswordSchema) -> SuccessResponse:
        """Reset password."""
        user_schema = await self.repository.get_by_email(schema.email)
        if not user_schema:
            raise UserNotFoundError
        code = await ConfirmationCodeService().verify_code(user_schema.user_id, schema.code)
        if not code:
            raise InvalidConfirmationCodeError
        hashed_password = HashService.hash_password(schema.password)
        await self.repository.change_password(user_schema.user_id, hashed_password)
        return SuccessResponse(success=True)
