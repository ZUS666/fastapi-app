from fastapi import APIRouter

from .auth_routers import auth_router
from .avatar_routers import avatar_router
from .user_ruoters import user_router


def get_routers_v1() -> APIRouter:
    router_v1 = APIRouter(prefix='/api/v1')
    router_v1.include_router(auth_router)
    router_v1.include_router(user_router)
    router_v1.include_router(avatar_router)
    return router_v1
