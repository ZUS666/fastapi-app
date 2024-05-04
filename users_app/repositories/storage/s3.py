from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING

from domain.constants.avatar_constants import AVATAR_BUCKET
from repositories.storage.s3client import ClientS3


if TYPE_CHECKING:
    from types_aiobotocore_s3 import S3Client


from repositories.storage.base import IStorage


class S3Storage(IStorage):
    def __init__(self) -> None:
        self._client: Callable[[], AbstractAsyncContextManager[S3Client]] = ClientS3().get

    async def upload_avatar(self, object: bytes, obj_name: str) -> None:
        async with self._client() as s3_client:
            await s3_client.put_object(Body=object, Bucket=AVATAR_BUCKET, Key=obj_name)
