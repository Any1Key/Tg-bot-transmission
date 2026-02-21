from __future__ import annotations

from pathlib import Path
from typing import Annotated
from urllib.parse import urlparse

import yaml
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    token: str = Field(alias="TOKEN")
    transmission_url: str = Field(alias="TRANSMISSION_URL")
    transmission_user: str = Field(alias="TRANSMISSION_USER")
    transmission_pass: str = Field(alias="TRANSMISSION_PASS")
    admin_user_ids: Annotated[list[int], NoDecode] = Field(alias="ADMIN_USER_IDS")
    database_url: str = Field(alias="DATABASE_URL", default="sqlite+aiosqlite:///./data/bot.db")
    config_path: str = Field(alias="CONFIG_PATH", default="/app/config.yml")
    poll_interval_seconds: int = Field(alias="POLL_INTERVAL_SECONDS", default=45)
    throttle_seconds: float = Field(alias="THROTTLE_SECONDS", default=1.0)
    log_level: str = Field(alias="LOG_LEVEL", default="INFO")

    @field_validator("admin_user_ids", mode="before")
    @classmethod
    def parse_admin_ids(cls, v: object) -> list[int]:
        if isinstance(v, str):
            return [int(x.strip()) for x in v.split(",") if x.strip()]
        if isinstance(v, int):
            return [v]
        if isinstance(v, list):
            return [int(x) for x in v]
        raise ValueError("invalid ADMIN_USER_IDS")

    @property
    def transmission_conn(self) -> dict[str, object]:
        p = urlparse(self.transmission_url)
        return {"protocol": p.scheme or "http", "host": p.hostname or "transmission", "port": p.port or 9091, "path": p.path or "/transmission/rpc"}


class YamlConfig(BaseModel):
    download_dirs: dict[str, str] = Field(default_factory=dict)


def load_yaml_config(path: str) -> YamlConfig:
    fp = Path(path)
    if not fp.exists():
        raise FileNotFoundError(path)
    raw = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
    return YamlConfig.model_validate(raw)
