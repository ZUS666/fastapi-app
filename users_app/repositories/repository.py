from abc import abstractmethod

from pydantic import EmailStr

from domain.custom_types.types_users import UIDType
from domain.schemas.user_schemas import (
    ProfileSchema,
    ProfileUpdateSchema,
    UserCredentialsSchema,
    UserInfoSchema,
    UserInfoSchemaActive,
    UserRegistrationInputSchema,
)


class IUserRepository:
    @abstractmethod
    async def get_by_email(self, email: EmailStr) -> UserCredentialsSchema | None:
        """Get user by email."""
        pass

    @abstractmethod
    async def create(self, user_schema: UserRegistrationInputSchema) -> UserInfoSchema | None:
        """Create a new user in db."""
        pass

    @abstractmethod
    async def get_user_info_by_id(self, user_id: UIDType) -> UserInfoSchema | None:
        """Get user info by id."""
        pass

    @abstractmethod
    async def get_user_info_by_email(self, email: EmailStr) -> UserInfoSchemaActive | None:
        """Get user info by email."""
        pass

    @abstractmethod
    async def update_profile(
        self, user_id: UIDType, profile_schema: ProfileUpdateSchema
    ) -> ProfileSchema | None:
        """Update user profile."""
        pass

    @abstractmethod
    async def activate_user(self, user_id: UIDType) -> None:
        """Activate user."""
        pass

    @abstractmethod
    async def change_password(self, user_id: UIDType, hashed_password: str) -> None:
        """Change password."""
        pass
