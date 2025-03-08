from typing import Literal

from pydantic import (
    BaseModel,
    PostgresDsn,
    RedisDsn,
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from dotenv import load_dotenv

load_dotenv("../.env")

LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 8000


class GunicornConfig(BaseModel):
    host: str = "localhost"
    port: int = 8000
    timeout: int = 900
    workers: int = 1


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    tasks: str = "/tasks"
    notes: str = "/notes"
    auth: str = "/auth"
    users: str = "/users"
    profiles: str = "/profiles"
    categories: str = "/categories"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()

    @property
    def bearer_token_url(self) -> str:
        # "api/v1/auth/login"
        parts = (self.prefix, self.v1.prefix, self.v1.auth, "/login")
        path = "".join(parts)
        return path.removeprefix("/")


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 50

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str


class EmailConfig(BaseModel):
    smtp_user: str
    smtp_password: str
    smtp_server: str
    smtp_port: str


class CeleryConfig(BaseModel):
    celery_broker_url: RedisDsn
    celery_result_backend: RedisDsn


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        env_file_encoding="utf-8",
    )

    run: RunConfig = RunConfig()
    gunicorn: GunicornConfig = GunicornConfig()
    logging: LoggingConfig = LoggingConfig()
    db: DatabaseConfig
    api: ApiPrefix = ApiPrefix()
    access_token: AccessToken
    email_a: EmailConfig
    celery: CeleryConfig


settings = Settings()
