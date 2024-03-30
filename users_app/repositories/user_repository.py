from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Database
from core.dependency import impl
from domain.custom_types.types_users import UIDType
from domain.schemas.user_schemas import (
    ProfileSchema,
    ProfileUpdateSchema,
    UserCredentialsSchema,
    UserInfoSchema,
    UserRegistrationInputSchema,
    UserSchema,
)
from repositories.cache.base_cache import IBaseCache
from repositories.repository import IUserRepository
from repositories.sql_db.models.user import Profile, User
from repositories.sql_db.user_db import UserPostgres


class UserRepository(IUserRepository):
    def __init__(self):
        self.cache = impl.container.resolve(IBaseCache)
        self.session: AsyncSession = Database().get_session()

    async def get_by_id(self, user_id: UIDType) -> UserSchema | None:
        user_cache: dict = await self.cache.get(str(user_id))
        if user_cache:
            return user_cache
        async with self.session as session:
            user: User = await UserPostgres(session).get_by_id(user_id)
        if not user:
            return None
        schema = UserSchema.model_validate(user)
        await self.cache.set(
            str(user_id),
            schema,
        )
        return schema

    async def get_by_email(self, email: EmailStr) -> UserCredentialsSchema | None:
        async with self.session as session:
            user: User = await UserPostgres(session).get_by_email(email)
        return (
            UserCredentialsSchema.model_validate(user, from_attributes=True)
            if user
            else None
        )

    async def create(
        self, user_schema: UserRegistrationInputSchema
    ) -> UserInfoSchema | None:
        async with self.session as session:
            db = UserPostgres(session)
            exists = await db.exists_by_email(user_schema.email)
            if exists:
                return None
            user = await db.create(user_schema)
            schema = UserInfoSchema.model_validate(user)
            await self.cache.set(
                key=str(schema.user_id),
                schema=schema,
            )
            return schema

    async def get_user_info_by_id(self, user_id: UIDType) -> UserInfoSchema:
        user_cache = await self.cache.get(str(user_id))
        if user_cache:
            return user_cache
        async with self.session as session:
            user: User = await UserPostgres(session).get_user_info_by_id(user_id)
        print(user)
        schema = UserInfoSchema.model_validate(user)
        await self.cache.set(str(user_id), schema)
        return schema

    async def update_profile(
        self, user_id: UIDType, profile_schema: ProfileUpdateSchema
    ) -> ProfileSchema:
        async with self.session as session:
            profile: Profile = await UserPostgres(session).update_profile(
                user_id, profile_schema
            )
        schema = ProfileSchema.model_validate(profile)
        user_cache = await self.cache.get(str(user_id))
        if user_cache:
            user_cache.profile = schema
            await self.cache.set(
                str(user_id),
                user_cache,
            )
        schema = ProfileSchema.model_validate(profile)
        return schema
