from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


ENV_FILE = '.env'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE, env_file_encoding='utf-8', case_sensitive=False, extra='ignore'
    )


class DBSettings(Settings):
    db_url: str
    db_echo: bool = False


class TokenSettings(Settings):
    secret_key: str


class MainSettings(BaseSettings):
    db: DBSettings
    token: TokenSettings


@lru_cache
def get_settings() -> MainSettings:
    return MainSettings(db=DBSettings(), token=TokenSettings())  # type: ignore [call-arg]


settings = get_settings()
