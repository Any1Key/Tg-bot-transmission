# Copyright (c) 2026 Any1Key
from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from bot.models.base import Base, utcnow


class Torrent(Base):
    __tablename__ = "torrents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    torrent_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    torrent_name: Mapped[str] = mapped_column(String(512))
    download_dir: Mapped[str | None] = mapped_column(String(512), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="added")
    notified: Mapped[bool] = mapped_column(Boolean, default=False)
    ratio: Mapped[float | None] = mapped_column(Float, nullable=True)
    size_bytes: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    download_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
