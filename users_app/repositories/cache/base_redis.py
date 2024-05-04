from repositories.cache.redis_connect import RedisCache


class RedisBaseCache:
    def __init__(self) -> None:
        self._connect = RedisCache.connect()
