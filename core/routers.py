from fastapi import APIRouter

from users.routers import router as users_router


router_v1 = APIRouter(prefix='/api/v1')
router_v1.include_router(users_router)
