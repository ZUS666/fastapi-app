from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


ENV_FILE = '.env_user_app'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE, env_file_encoding='utf-8', case_sensitive=False, extra='ignore'
    )


class DBSettings(Settings):
    db_url: str
    db_echo: bool = False


class RedisSettings(Settings):
    redis_url: str
    redis_max_connections: int = 10


class TokenSettings(Settings):
    secret_key: str


class AMQPSettings(Settings):
    amqp_url: str


class StorageSettings(Settings):
    storage_path: str
    s3_key: str
    s3_secret: str
    s3_region_name: str


class MainSettings(BaseSettings):
    db: DBSettings
    token: TokenSettings
    redis: RedisSettings
    amqp: AMQPSettings
    storage: StorageSettings


@lru_cache
def get_settings() -> MainSettings:
    return MainSettings(
        db=DBSettings(),
        token=TokenSettings(),
        redis=RedisSettings(),
        amqp=AMQPSettings(),
        storage=StorageSettings(),
    )  # type: ignore [call-arg]


settings = get_settings()
