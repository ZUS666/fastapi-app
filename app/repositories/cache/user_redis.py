from domain.constants.user_constants import CacheName, CacheTimeout
from domain.schemas.user_schemas import UserInfoSchema
from repositories.cache.base_cache import IUserBaseCache
from repositories.cache.base_redis import RedisBaseCache


class UserRedisCache(IUserBaseCache, RedisBaseCache):
    async def get(self, key: str) -> UserInfoSchema:
        json_schema = await self.connect.get(
            name=CacheName.USER_INFO.value.format(str(key)),
        )
        return UserInfoSchema.model_validate_json(json_schema) if json_schema else None
    
    async def set(self, key: str, schema: UserInfoSchema) -> None:
        await self.connect.set(
            name=CacheName.USER_INFO.value.format(key),
            value=schema.model_dump_json(),
            ex=CacheTimeout.USER_INFO.value,
        )

    async def delete(self, key: str) -> None:
        await self.connect.delete(key=CacheName.USER_INFO.value.format(key))
