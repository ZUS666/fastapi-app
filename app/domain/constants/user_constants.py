import enum


HASH_SCHEMA: str = 'bcrypt'
LEN_CONFIRMATION_CODE: int = 6


class CacheName(enum.StrEnum):
    USER_INFO = 'user_info:{}'
    CONFIRMATION_CODE = 'user_code:{}'


class CacheTimeout(enum.IntEnum):
    USER_INFO = 12 * 60 * 60
    CONFIRMATION_CODE = 10 * 60


class MaxLength(enum.IntEnum):
    FIRST_NAME = 100
    LAST_NAME = 100
