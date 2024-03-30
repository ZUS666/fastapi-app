from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.settings import settings


class Database:
    def __init__(self) -> None:
        self.engine = create_async_engine(
            url=settings.db.db_url,
            echo=settings.db.db_echo,
        )
        self.session = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session() as session:
            try:
                print(f'get_session {type(session)}')
                yield session
            except exc.SQLAlchemyError as error:
                print('ROLLBACK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                await session.rollback()
                raise error
