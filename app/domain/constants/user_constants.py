import enum


HASH_SCHEMA: str = 'bcrypt'

class CacheName(enum.StrEnum):
    USER_INFO = 'user_info:{}'

class CacheTimeout(enum.IntEnum):
    USER_INFO = 60 * 60 * 12

class MaxLength(enum.IntEnum):
    FIRST_NAME = 100
    LAST_NAME = 100