from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from domain.schemas.avatar_schemas import AvatarSchema
from domain.schemas.common_schemas import SuccessResponse
from domain.services.auth_service import PermissionService
from domain.services.avatar_service import UserAvatarSetService


avatar_router = APIRouter(prefix='/avatars', tags=['avatars'])


@avatar_router.post('')
async def set_avatar(
    file: UploadFile,
    auth_headers: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    service: Annotated[UserAvatarSetService, Depends(UserAvatarSetService)],
) -> SuccessResponse:
    user_id = PermissionService.get_current_user_id(auth_headers.credentials)
    schema = AvatarSchema(
        file_bytes=await file.read(),
        file_size=file.size,
        mime_type=file.content_type,
    )
    return await service.set(user_id, schema)
