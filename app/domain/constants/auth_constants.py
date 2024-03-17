import enum


class TokenEnum(enum.Enum):
    ALGORITHM: str = 'HS256'
    refresh: str = 'refresh'
    access: str = 'access'
    access_token_expires: int = 60 * 60 * 24
    refresh_token_expires: int = 60 * 60 * 24 * 7