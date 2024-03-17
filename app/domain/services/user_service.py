import bcrypt

from core.dependency import impl
from domain.custom_types.types_users import UIDType
from domain.exceptions.user_exceptions import (
    InvalidPasswordError,
    UserAlreadyExistError,
    UserNotFoundError,
)
from domain.schemas.auth_schemas import TokenResponseSchema
from domain.schemas.user_schemas import (
    ProfileSchema,
    ProfileUpdateSchema,
    UserCredentialsSchema,
    UserInfoSchema,
    UserLoginSchema,
    UserRegistrationInputSchema,
)
from domain.services.auth_service import JWTService
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

    async def create(
        self,
        user: UserRegistrationInputSchema
    ) -> UserInfoSchema:
        """Create new user in database."""
        user.password = HashService.hash_password(user.password)
        user_model = await self.repository.create(user)
        if not user_model:
            raise UserAlreadyExistError
        return user_model

    async def login(
        self,
        user_login: UserLoginSchema,
    ) -> TokenResponseSchema:
        """Login user."""
        user: UserCredentialsSchema = await self.repository.get_by_email(user_login.email)
        if not user:
            raise UserNotFoundError
        if not HashService.verify_password(user_login.password, user.password):
            raise InvalidPasswordError
        return JWTService.create_tokens(user.user_id)

    async def get_user_info(
        self,
        user_id: UIDType
    ) -> UserInfoSchema:
        """Get user info."""
        user = await self.repository.get_user_info_by_id(user_id)
        if not user:
            raise UserNotFoundError
        return UserInfoSchema.model_validate(user)

    async def update_profile(
        self,
        user_id: UIDType,
        profile: ProfileUpdateSchema
    ) -> ProfileSchema:
        return await self.repository.update_profile(user_id, profile)
