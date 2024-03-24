from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


ENV_FILE = '.env_notify'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE, env_file_encoding='utf-8', case_sensitive=False, extra='ignore'
    )


class SMTPSettings(Settings):
    email_host: str
    email_username: str
    email_password: str
    email_port: int
    email_use_tls: bool = False


class AMQPSettings(Settings):
    amqp_url: str


class MainSettings(Settings):
    smtp: SMTPSettings
    amqp: AMQPSettings


@lru_cache
def get_settings() -> MainSettings:
    return MainSettings(smtp=SMTPSettings(), amqp=AMQPSettings())  # type: ignore [call-arg]


settings = get_settings()
