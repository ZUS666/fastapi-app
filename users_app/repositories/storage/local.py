from pathlib import Path

import aiofiles

from domain.constants.avatar_constants import AVATAR_BUCKET
from repositories.storage.base import IStorage


class LocalStorage(IStorage):
    async def upload_avatar(self, object: bytes, obj_name: str) -> None:
        self._create_folder()
        async with aiofiles.open(Path(AVATAR_BUCKET) / obj_name, 'wb+') as file:
            await file.write(object)

    @staticmethod
    def _create_folder() -> None:
        Path(AVATAR_BUCKET).mkdir(parents=True, exist_ok=True)
