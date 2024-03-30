from fastapi import FastAPI

from adapters.broker.notify_base import INotifyService
from adapters.broker.rabbitmq.rabbit_notify import RabbitMQNotifyService
from api.v1.routers import router_v1
from core.dependency import impl
from core.exception_handler import ExceptionHandlerMiddleware
from repositories.cache.base_cache import IUserBaseCache, IUserCodeCache
from repositories.cache.user_redis import UserCodeRedisCache, UserRedisCache
from repositories.repository import IUserRepository
from repositories.sql_db.admin.sql_admin import build_admin
from repositories.user_repository import UserRepository


def build_app() -> FastAPI:
    injections = (
        (IUserRepository, UserRepository),
        (IUserBaseCache, UserRedisCache),
        (INotifyService, RabbitMQNotifyService),
        (IUserCodeCache, UserCodeRedisCache),
    )
    impl.register_all(injections)
    app = FastAPI()
    build_admin(app)
    app.include_router(router_v1)
    app.add_middleware(ExceptionHandlerMiddleware)
    return app
