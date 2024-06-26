from pydantic import EmailStr
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from domain.custom_types.types_users import UIDType
from domain.schemas.user_schemas import ProfileUpdateSchema, UserRegistrationInputSchema
from repositories.sql_db.models import Profile, User


class UserPostgres:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UIDType) -> User | None:
        """Get user by id."""
        user = await self.session.get(User, user_id)
        return user

    async def get_by_email(self, email: EmailStr) -> User | None:
        """Get user by email."""
        stmt = select(User).where(User.email == email)
        user = await self.session.scalar(statement=stmt)
        return user

    async def exists_by_email(self, email: EmailStr) -> bool:
        """Check if user exists by email."""
        stmt = select(select(User).where(User.email == email).exists())
        user = await self.session.scalar(statement=stmt)
        return True if user else False

    async def create(self, user_schema: UserRegistrationInputSchema) -> User:
        """Create a new user in db."""
        user = User(**user_schema.model_dump(exclude={'re_password', 'profile'}))
        profile = Profile(
            user=user, **user_schema.profile.model_dump() if user_schema.profile else {}
        )
        user.profile = profile
        self.session.add(user)
        await self.session.commit()
        return user

    async def get_user_info_by_id(self, user_id: UIDType) -> User | None:
        """Get user info by id."""
        stmt = (
            select(User)
            .options(joinedload(User.profile, innerjoin=True))
            .where(User.user_id == user_id)
        )
        return await self.session.scalar(statement=stmt)

    async def get_user_info_by_email(self, email: EmailStr) -> User | None:
        """"Get user info by email."""
        stmt = (
            select(User)
            .where(User.email == email)
            .options(joinedload(User.profile, innerjoin=True))
        )
        return await self.session.scalar(statement=stmt)

    async def update_profile(
        self, user_id: UIDType, profile_schema: ProfileUpdateSchema
    ) -> Profile | None:
        stmt = (
            update(Profile)
            .where(Profile.user_id == user_id)
            .values(**profile_schema.model_dump(
                exclude_none=True,
                include={'first_name', 'last_name'})
                )
            .returning(Profile)
        )
        profile = await self.session.scalar(statement=stmt)
        await self.session.commit()
        return profile

    async def activate_user(self, user_id: UIDType) -> None:
        stmt = update(User).where(User.user_id == user_id).values(is_active=True)
        await self.session.execute(statement=stmt)
        await self.session.commit()

    async def change_password(self, user_id: UIDType, new_password: str) -> None:
        stmt = update(User).where(User.user_id == user_id).values(password=new_password)
        await self.session.execute(statement=stmt)
        await self.session.commit()

    async def update_user_avatar(self, user_id: UIDType, avatar_name: str) -> None:
        stmt = update(Profile).where(Profile.user_id == user_id).values(avatar=avatar_name)
        await self.session.execute(statement=stmt)
        await self.session.commit()
