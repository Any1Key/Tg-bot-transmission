# Copyright (c) 2026 Any1Key
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from bot.i18n import normalize_lang
from bot.models.base import utcnow
from bot.models.torrent import Torrent
from bot.models.user_setting import UserSetting


def make_session_factory(database_url: str) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(database_url, echo=False)
    return async_sessionmaker(engine, expire_on_commit=False)


class DBService:
    def __init__(self, sf: async_sessionmaker[AsyncSession]) -> None:
        self.sf = sf

    async def add_torrent(self, user_id: int, torrent_hash: str, torrent_name: str) -> None:
        async with self.sf() as s:
            s.add(Torrent(user_id=user_id, torrent_hash=torrent_hash, torrent_name=torrent_name, status="added", notified=False))
            try:
                await s.commit()
            except IntegrityError:
                await s.rollback()
                existing = await s.scalar(select(Torrent).where(Torrent.torrent_hash == torrent_hash))
                if not existing or int(existing.user_id) != int(user_id):
                    raise ValueError("torrent_already_exists")

                # Активную задачу не дублируем, но разрешаем пере-добавление
                # старых/завершенных/missing записей тем же пользователем.
                if existing.status in {"added", "downloading"} and not existing.notified:
                    raise ValueError("torrent_already_exists")

                existing.torrent_name = torrent_name
                existing.download_dir = None
                existing.status = "added"
                existing.notified = False
                existing.ratio = None
                existing.size_bytes = None
                existing.download_seconds = None
                existing.completed_at = None
                existing.added_at = utcnow()
                await s.commit()

    async def set_torrent_dir(self, torrent_hash: str, download_dir: str) -> None:
        async with self.sf() as s:
            await s.execute(update(Torrent).where(Torrent.torrent_hash == torrent_hash).values(download_dir=download_dir, status="downloading"))
            await s.commit()

    async def get_user_torrent_status(self, user_id: int, torrent_hash: str) -> str | None:
        async with self.sf() as s:
            return await s.scalar(
                select(Torrent.status).where(
                    Torrent.user_id == user_id,
                    Torrent.torrent_hash == torrent_hash,
                )
            )

    async def delete_user_torrent(self, user_id: int, torrent_hash: str) -> int:
        async with self.sf() as s:
            res = await s.execute(
                delete(Torrent).where(
                    Torrent.user_id == user_id,
                    Torrent.torrent_hash == torrent_hash,
                )
            )
            await s.commit()
            return int(res.rowcount or 0)

    async def get_pending(self) -> list[Torrent]:
        async with self.sf() as s:
            rows = await s.scalars(select(Torrent).where(Torrent.notified.is_(False)))
            return list(rows)

    async def complete(self, torrent_hash: str, ratio: float | None, size: int | None, secs: int | None) -> None:
        async with self.sf() as s:
            await s.execute(update(Torrent).where(Torrent.torrent_hash == torrent_hash).values(status="completed", notified=True, ratio=ratio, size_bytes=size, download_seconds=secs, completed_at=func.now()))
            await s.commit()

    async def mark_missing(self, torrent_hash: str) -> None:
        async with self.sf() as s:
            await s.execute(
                update(Torrent)
                .where(Torrent.torrent_hash == torrent_hash)
                .values(status="missing", notified=True)
            )
            await s.commit()

    async def cleanup_missing(self) -> int:
        async with self.sf() as s:
            res = await s.execute(delete(Torrent).where(Torrent.status == "missing"))
            await s.commit()
            return int(res.rowcount or 0)

    async def cleanup_stale_pending(self, stale_hours: int) -> int:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=stale_hours)
        async with self.sf() as s:
            res = await s.execute(
                delete(Torrent).where(
                    Torrent.notified.is_(False),
                    Torrent.added_at < cutoff,
                )
            )
            await s.commit()
            return int(res.rowcount or 0)

    async def history(self, user_id: int, page: int, page_size: int) -> tuple[list[Torrent], int]:
        async with self.sf() as s:
            total = int((await s.execute(select(func.count()).select_from(Torrent).where(Torrent.user_id == user_id))).scalar_one())
            rows = await s.scalars(select(Torrent).where(Torrent.user_id == user_id).order_by(Torrent.added_at.desc()).offset((page-1)*page_size).limit(page_size))
            return list(rows), total

    async def ensure_user_lang(self, user_id: int, raw_lang: str | None) -> str:
        async with self.sf() as s:
            row = await s.scalar(select(UserSetting).where(UserSetting.user_id == user_id))
            if row:
                return normalize_lang(row.lang)
            lang = normalize_lang(raw_lang)
            s.add(UserSetting(user_id=user_id, lang=lang))
            await s.commit()
            return lang

    async def set_user_lang(self, user_id: int, lang: str) -> str:
        norm = normalize_lang(lang)
        async with self.sf() as s:
            row = await s.scalar(select(UserSetting).where(UserSetting.user_id == user_id))
            if row:
                row.lang = norm
            else:
                s.add(UserSetting(user_id=user_id, lang=norm))
            await s.commit()
        return norm
