from functools import lru_cache
from typing import Literal
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class ConfigBase(BaseSettings):
    """Базовый класс для всех конфигов."""
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )



class EnvironmentConfig(ConfigBase):
    """Определяет текущее окружение приложения."""
    model_config = SettingsConfigDict(env_prefix="APP_")

    env: Literal["dev", "prod", "test"] = "dev"
    debug: bool = True



class TelegramConfig(ConfigBase):
    model_config = SettingsConfigDict(
        env_prefix="TG_",
        env_file=".env",
    )

    bot_token: str
    bot_id: int


class RedisConfig(ConfigBase):
    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
        env_file=".env",
    )

    host: str = "localhost"
    port: int = 6379
    db: int = 0


class DBConfig(ConfigBase):
    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
    )

    url: str
    pool_size: int = 10

class WebConfig(ConfigBase):
    model_config = SettingsConfigDict(
        env_prefix="WEB_",
        env_file=".env"
    )
    host: str = "localhost"
    port: int = 1255


# === ГЛАВНАЯ КОНФИГУРАЦИЯ ===

class Config(BaseModel):
    """Объединённая конфигурация проекта."""
    env: EnvironmentConfig
    telegram: TelegramConfig
    db: DBConfig
    redis: RedisConfig
    web: WebConfig

    @classmethod
    @lru_cache
    def load(cls) -> "Config":
        """
        Загружает все конфиги из соответствующего .env-файла и кэширует результат.
        Выбирает .env автоматически по окружению (например: .env.prod, .env.dev).
        """
        env_cfg = EnvironmentConfig()
        if env_cfg.env == "dev":
            env_file = ".env.dev"
        else:
            env_file = f".env.{env_cfg.env}"
        telegram = TelegramConfig(_env_file=env_file)
        db = DBConfig(_env_file=env_file)
        redis = RedisConfig(_env_file=env_file)
        web = WebConfig(_env_file=env_file)

        return cls(env=env_cfg, telegram=telegram, db=db, redis=redis, web=web)
