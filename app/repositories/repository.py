from abc import abstractmethod

from pydantic import EmailStr

from domain.custom_types.types_users import UIDType
from domain.schemas.user_schemas import (
    ProfileUpdateSchema,
    UserInfoSchema,
    UserRegistrationInputSchema,
    UserSchema,
)


class IUserRepository:
    @abstractmethod
    async def get_by_id(self, user_id: UIDType) -> UserSchema | None:
        """Get user by id."""
        pass

    @abstractmethod
    async def get_by_email(self, email: EmailStr) -> UserSchema | None:
        """Get user by email."""
        pass

    # @abstractmethod
    # async def exists_by_email(self, email: EmailStr) -> bool | None:
    #     """Check if user exists by email."""
    #     pass

    @abstractmethod
    async def create(self, user_schema: UserRegistrationInputSchema) -> UserInfoSchema:
        """Create a new user in db."""
        pass

    @abstractmethod
    async def get_user_info_by_id(self, user_id: UIDType) -> UserInfoSchema | None:
        """Get user info by id."""
        pass

    @abstractmethod
    async def update_profile(
        self,
        user_id: UIDType,
        profile_schema: ProfileUpdateSchema
    ) -> UserInfoSchema:
        """Update user profile."""
        pass
