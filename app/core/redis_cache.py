from redis import asyncio as redis

from core.settings import settings


class RedisCache:
    @staticmethod
    def connect():
        pool = redis.ConnectionPool.from_url(settings.redis.redis_url)
        return redis.Redis(
            connection_pool=pool,
            max_connections=settings.redis.redis_max_connections,
        )
