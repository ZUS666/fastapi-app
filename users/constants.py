import enum


class UsersOrderBy(enum.StrEnum):
    user_id = 'user_id'
    email = 'email'


class ExceptionMessage(enum.StrEnum):
    USER_NOT_FOUND = 'User not found'
    USER_ALREADY_EXISTS = 'User already exists'
    PASSWORD_REGEX = (
        'Password must contain at least one uppercase letter, one lowercase letter, '
        'one number, and one special character'
    )
    INVALID_PASSWORD = 'Invalid password'
    INVALID_TOKEN = 'Invalid token'


class TokenEnum(enum.Enum):
    ALGORITHM: str = 'HS256'
    refresh: str = 'refresh'
    access: str = 'access'
    access_token_expires: int = 60 * 60 * 24
    refresh_token_expires: int = 60 * 60 * 24 * 7
