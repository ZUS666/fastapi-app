from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependency import impl
from domain.custom_types.types_users import UIDType
from domain.schemas.user_schemas import (
    ProfileSchema,
    ProfileUpdateSchema,
    UserCredentialsSchema,
    UserInfoSchema,
    UserInfoSchemaActive,
    UserRegistrationInputSchema,
)
from repositories.cache.base_cache import IUserBaseCache
from repositories.repository import IUserRepository
from repositories.sql_db.models.user import Profile, User
from repositories.sql_db.session import Database
from repositories.sql_db.user_db import UserPostgres


class UserRepository(IUserRepository):
    def __init__(self):
        self.cache: IUserBaseCache = impl.container.resolve(IUserBaseCache)
        self.session: Callable[
            [], AbstractAsyncContextManager[AsyncSession]
        ] = Database().get_session

    async def get_by_email(self, email: EmailStr) -> UserCredentialsSchema | None:
        async with self.session() as session:
            user: User | None = await UserPostgres(session).get_by_email(email)
        return (
            UserCredentialsSchema.model_validate(user, from_attributes=True)
            if user else None
        )

    async def create(
        self,
        user_schema: UserRegistrationInputSchema
    ) -> UserInfoSchema | None:
        async with self.session() as session:
            db = UserPostgres(session)
            exists = await db.exists_by_email(user_schema.email)
            if exists:
                return None
            user = await db.create(user_schema)
        schema = UserInfoSchema.model_validate(user, from_attributes=True)
        await self.cache.set(key=str(schema.user_id), schema=schema,)
        return schema

    async def get_user_info_by_id(self, user_id: UIDType) -> UserInfoSchema | None:
        user_cache = await self.cache.get(str(user_id))
        if user_cache:
            return user_cache
        async with self.session() as session:
            user: User | None = await UserPostgres(session).get_user_info_by_id(user_id)
        if not user:
            return None
        schema = UserInfoSchema.model_validate(user, from_attributes=True)
        await self.cache.set(str(user_id), schema)
        return schema

    async def get_user_info_by_email(self, email: EmailStr) -> UserInfoSchemaActive | None:
        async with self.session() as session:
            db = UserPostgres(session)
            user = await db.get_user_info_by_email(email)
        if not user:
            return None
        user_schema = UserInfoSchemaActive.model_validate(user, from_attributes=True)
        await self.cache.set(
            str(user_schema.user_id),
            UserInfoSchema.model_construct(**user_schema.model_dump()),
        )
        return user_schema

    async def update_profile(
        self,
        user_id: UIDType,
        profile_schema: ProfileUpdateSchema
    ) -> ProfileSchema | None:
        async with self.session() as session:
            profile: Profile | None = await UserPostgres(session).update_profile(
                user_id, profile_schema
            )
        if not profile:
            return None
        schema = ProfileSchema.model_validate(profile, from_attributes=True)
        user_cache = await self.cache.get(str(user_id))
        if user_cache:
            user_cache.profile = schema
            await self.cache.set(
                str(user_id),
                user_cache,
            )
        schema = ProfileSchema.model_validate(profile, from_attributes=True)
        return schema

    async def activate_user(self, user_id: UIDType) -> None:
        async with self.session() as session:
            db = UserPostgres(session)
            await db.activate_user(user_id)
