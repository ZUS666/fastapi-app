import hashlib
import mimetypes

from core.dependency import impl
from domain.constants.avatar_constants import AvatarAllowTypes
from domain.custom_types.types_users import UIDType
from domain.schemas.avatar_schemas import AvatarSchema
from domain.schemas.common_schemas import SuccessResponse
from repositories.repository import IUserRepository
from repositories.storage.base import IStorage


class UserAvatarSetService:
    def __init__(self) -> None:
        self._storage_adapter: IStorage = impl.container.resolve(IStorage)
        self._repository: IUserRepository = impl.container.resolve(IUserRepository)

    async def set(self, user_id: UIDType, schema: AvatarSchema) -> SuccessResponse:
        filename = self._get_hashed_filename(user_id, schema.mime_type)
        await self._storage_adapter.upload_avatar(
            schema.file_bytes,
            filename,
        )
        await self._repository.update_user_avatar(user_id, filename)
        return SuccessResponse(success=True)

    def _get_hashed_filename(self, user_id: UIDType, mime_type: AvatarAllowTypes) -> str:
        hashed_name = hashlib.sha1(str(user_id).encode()).hexdigest()
        ext = mimetypes.guess_extension(mime_type, strict=True)
        return ''.join([hashed_name, ext])
