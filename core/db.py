from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .settings import settings


class Database:
    def __init__(self) -> None:
        self.engine = create_async_engine(
            url=settings.DB_URL,
            echo=settings.DB_ECHO,
        )
        self.session = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )


db = Database()
