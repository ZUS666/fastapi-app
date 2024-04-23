from typing import Annotated

from pydantic import BaseModel, Field

from domain.constants.avatar_constants import AVATAR_MAX_SIZE, AvatarAllowTypes


class AvatarSchema(BaseModel):
    file_bytes: bytes
    file_size: Annotated[int, Field(le=AVATAR_MAX_SIZE)]
    mime_type: AvatarAllowTypes
