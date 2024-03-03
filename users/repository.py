from typing import Annotated, Sequence

from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import Database
from core.models import Profile, User
from users.schemas import UserQueriesSchema, UserRegistrationSchema


class UserRepository:
    def __init__(
        self, session: Annotated[AsyncSession, Depends(Database().get_session)]
    ) -> None:
        self.session = session

    async def list(
        self,
        queries: UserQueriesSchema,
    ) -> Sequence[User]:
        """Get collction of users matching the given queries."""
        stmt = (
            select(User)
            .limit(queries.limit)
            .offset(queries.offset)
            .order_by(queries.order_by)
        )
        users = await self.session.scalars(statement=stmt)
        return users.all()

    async def get_by_id(self, id: int) -> User | None:
        """Get user by id."""
        user = await self.session.get(User, id)
        return user

    async def get_by_email(self, email: EmailStr) -> User | None:
        """Get user by email."""
        stmt = select(User).where(User.email == email)
        user = await self.session.scalar(statement=stmt)
        return user

    async def exists_by_email(self, email: EmailStr) -> bool | None:
        """Check if user exists by email."""
        stmt = select(select(User).where(User.email == email).exists())
        user = await self.session.scalar(statement=stmt)
        return user

    async def create(self, user_schema: UserRegistrationSchema) -> User:
        """Create a new user in db."""
        user = User(**user_schema.model_dump(exclude={'re_password'}))
        profile = Profile(user=user, **user_schema.profile.model_dump() if user_schema.profile else {})
        user.profile = profile
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
