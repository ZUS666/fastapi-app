from core.redis_cache import RedisCache


class RedisBaseCache:
    def __init__(self) -> None:
        self.connect = RedisCache.connect()
