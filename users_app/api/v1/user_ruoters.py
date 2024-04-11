from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from domain.schemas.user_schemas import (
    ConfirmationUserSchema,
    EmailSchema,
    ProfileSchema,
    ProfileUpdateSchema,
    ResetPasswordSchema,
    SuccessResponse,
    UserInfoSchema,
    UserRegistrationInputSchema,
)
from domain.services.auth_service import PermissionService
from domain.services.user_service import UserService


user_router = APIRouter(prefix='/users', tags=['users'])


@user_router.post('/signup', status_code=201)
async def create_user(
    regigration_schema: UserRegistrationInputSchema,
    service: Annotated[UserService, Depends(UserService)],
) -> UserInfoSchema:
    """Register new user."""
    return await service.create(regigration_schema)


@user_router.get('/me')
async def get_current_user_info(
    auth_headers: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    service: Annotated[UserService, Depends(UserService)],
) -> UserInfoSchema:
    """Get current user info."""
    user_id = PermissionService.get_current_user_id(auth_headers.credentials)
    return await service.get_user_info_by_id(user_id)


@user_router.patch('/me')
async def update_current_user_info(
    auth_headers: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    profile_update_schema: ProfileUpdateSchema,
    service: Annotated[UserService, Depends(UserService)],
) -> ProfileSchema:
    """Update current user info."""
    user_id = PermissionService.get_current_user_id(auth_headers.credentials)
    return await service.update_profile(user_id, profile_update_schema)


@user_router.post('/resend_activation')
async def reconfirmation(
    email: EmailSchema,
    service: Annotated[UserService, Depends(UserService)],
) -> SuccessResponse:
    """Resend activation code."""
    return await service.resend_activation(email)


@user_router.post('/activation')
async def activation(
    schema: ConfirmationUserSchema,
    service: Annotated[UserService, Depends(UserService)],
) -> SuccessResponse:
    """Activation user."""
    return await service.activate_user(schema)


@user_router.post('/reset_password_request')
async def reset_password_request(
    email: EmailSchema,
    service: Annotated[UserService, Depends(UserService)],
) -> SuccessResponse:
    """Request to reset password."""
    return await service.reset_password_request(email)


@user_router.post('/reset_password')
async def reset_password(
    schema: ResetPasswordSchema,
    service: Annotated[UserService, Depends(UserService)],
) -> SuccessResponse:
    """Reset password with confirmation code from email."""
    return await service.reset_password(schema)
