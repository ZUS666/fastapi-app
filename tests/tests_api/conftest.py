import os
from collections.abc import AsyncGenerator
from typing import Any

import pytest
from alembic.command import downgrade, upgrade
from alembic.config import Config as Alembic
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from adapters.broker.mock.mock_notify import MockNotifyService
from adapters.broker.notify_base import INotifyService
from api.v1.routers import get_routers_v1
from core.dependency import impl
from core.exception_handler import ExceptionHandlerMiddleware
from domain.services.user_service import HashService
from repositories.cache.base_cache import IUserBaseCache, IUserCodeCache
from repositories.cache.user_redis import UserCodeRedisCache, UserRedisCache
from repositories.repository import IUserRepository
from repositories.sql_db.models import User
from repositories.sql_db.models.user import Profile
from repositories.sql_db.session import Database
from repositories.storage.base import IStorage
from repositories.storage.local import LocalStorage
from repositories.user_repository import UserRepository


def build_test_app() -> FastAPI:
    os.environ['db_url'] = 'postgresql+asyncpg://admin:password@localhost:5432/testdb'
    os.environ['redis_url'] = 'redis://localhost:6379/1'
    injections = (
        (IUserRepository, UserRepository),
        (IUserBaseCache, UserRedisCache),
        (INotifyService, MockNotifyService),
        (IUserCodeCache, UserCodeRedisCache),
        (IStorage, LocalStorage),
    )
    impl.register_all(injections)
    app = FastAPI()
    app.include_router(get_routers_v1())
    app.add_middleware(ExceptionHandlerMiddleware)
    return app


@pytest.fixture(scope="session", autouse=True)
def tables():
    alembic = Alembic('users_app/alembic.ini')
    alembic.set_main_option('script_location', 'users_app/repositories/sql_db/migrations/')
    upgrade(alembic, "head")
    yield
    downgrade(alembic, "base")


@pytest.fixture(scope="function")
async def active_user():
    """User fixture with is_active=True."""
    hashed_pw = HashService.hash_password('fakepass')
    active = User(
        email='active@main.com',
        password=hashed_pw,
        is_active=True,
    )
    active.profile = Profile(first_name='test', last_name='test')
    async with Database().get_session() as db:
        db.add(active)
        await db.commit()
        return active


@pytest.fixture(scope="function")
async def inactive_user():
    """User fixture with is_active=False."""
    hashed_pw = HashService.hash_password('fakepass')
    inactive = User(
        email='inactive@main.com',
        password=hashed_pw,
        is_active=False,
    )
    inactive.profile = Profile(first_name='test', last_name='test')
    async with Database().get_session() as db:
        db.add(inactive)
        await db.commit()
        return inactive


@pytest.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, Any]:
    """Test client."""
    async with AsyncClient(
        transport=ASGITransport(app=build_test_app()), base_url="http://test/api/v1"
    ) as client:
        yield client
