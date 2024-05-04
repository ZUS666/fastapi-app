from domain.constants.user_constants import CacheName, CacheTimeout
from domain.schemas.user_schemas import UserInfoSchema
from repositories.cache.base_cache import IUserBaseCache, IUserCodeCache
from repositories.cache.base_redis import RedisBaseCache


class UserRedisCache(IUserBaseCache, RedisBaseCache):
    async def get(self, key: str) -> UserInfoSchema | None:
        json_schema = await self._connect.get(
            name=CacheName.USER_INFO.value.format(str(key)),
        )
        return UserInfoSchema.model_validate_json(json_schema) if json_schema else None

    async def set(self, key: str, schema: UserInfoSchema) -> None:
        await self._connect.set(
            name=CacheName.USER_INFO.value.format(key),
            value=schema.model_dump_json(),
            ex=CacheTimeout.USER_INFO.value,
        )


class UserCodeRedisCache(IUserCodeCache, RedisBaseCache):
    async def get(self, key: str) -> str | None:
        code: bytes | None = await self._connect.get(
            name=CacheName.CONFIRMATION_CODE.value.format(str(key)),
        )
        return code.decode() if code else None

    async def set(self, key: str, code: str) -> None:
        await self._connect.set(
            name=CacheName.CONFIRMATION_CODE.value.format(key),
            value=code,
            ex=CacheTimeout.CONFIRMATION_CODE.value,
        )
