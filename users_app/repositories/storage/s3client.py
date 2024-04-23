import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import aioboto3
from types_aiobotocore_s3 import S3Client

from core.settings import settings


class ClientS3:
    def __init__(self) -> None:
        self._url = settings.storage.storage_path
        self._key = settings.storage.s3_key
        self._secret = settings.storage.s3_secret
        self._region_name = settings.storage.s3_region_name
        self._session: aioboto3.Session = aioboto3.Session(
            aws_access_key_id=self._key,
            aws_secret_access_key=self._secret,
            region_name=self._region_name,
        )

    @asynccontextmanager
    async def get(self) -> AsyncGenerator[S3Client, None]:
        async with self._session.client('s3', endpoint_url=self._url) as s3:
            yield s3
            logging.info('S3 client closed.')
