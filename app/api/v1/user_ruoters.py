from typing import Annotated

from fastapi import APIRouter, Depends

from domain.custom_types.types_users import UIDType
from domain.schemas.user_schemas import (
    ProfileSchema,
    ProfileUpdateSchema,
    UserInfoSchema,
    UserRegistrationInputSchema,
)
from domain.services.auth_service import PermissionService
from domain.services.user_service import UserService


user_router = APIRouter(prefix='/users')


@user_router.post('/signup/')
async def create_user(
    regigration_schema: UserRegistrationInputSchema,
    service: Annotated[UserService, Depends(UserService)],
) -> UserInfoSchema:
    """Register new user."""
    return await service.create(regigration_schema)

@user_router.get('/me/')
async def get_current_user_info(
    user_id: Annotated[UIDType, Depends(PermissionService.get_current_user_id)],
    service: Annotated[UserService, Depends(UserService)]
) -> UserInfoSchema:
    """Get current user info."""
    return await service.get_user_info(user_id)

@user_router.patch('/me/')
async def update_current_user_info(
    user_id: Annotated[UIDType, Depends(PermissionService.get_current_user_id)],
    profile_update_schema: ProfileUpdateSchema,
    service: Annotated[UserService, Depends(UserService)]
) -> ProfileSchema:
    """Update current user info."""
    return await service.update_profile(user_id,profile_update_schema)