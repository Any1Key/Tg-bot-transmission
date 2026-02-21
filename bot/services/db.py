from __future__ import annotations

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from bot.models.download_dir import DownloadDir
from bot.models.torrent import Torrent


def make_session_factory(database_url: str) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(database_url, echo=False)
    return async_sessionmaker(engine, expire_on_commit=False)


class DBService:
    def __init__(self, sf: async_sessionmaker[AsyncSession]) -> None:
        self.sf = sf

    async def add_torrent(self, user_id: int, torrent_hash: str, torrent_name: str) -> None:
        async with self.sf() as s:
            s.add(Torrent(user_id=user_id, torrent_hash=torrent_hash, torrent_name=torrent_name, status="added", notified=False))
            await s.commit()

    async def set_torrent_dir(self, torrent_hash: str, download_dir: str) -> None:
        async with self.sf() as s:
            await s.execute(update(Torrent).where(Torrent.torrent_hash == torrent_hash).values(download_dir=download_dir, status="downloading"))
            await s.commit()

    async def get_pending(self) -> list[Torrent]:
        async with self.sf() as s:
            rows = await s.scalars(select(Torrent).where(Torrent.notified.is_(False)))
            return list(rows)

    async def complete(self, torrent_hash: str, ratio: float | None, size: int | None, secs: int | None) -> None:
        async with self.sf() as s:
            await s.execute(update(Torrent).where(Torrent.torrent_hash == torrent_hash).values(status="completed", notified=True, ratio=ratio, size_bytes=size, download_seconds=secs, completed_at=func.now()))
            await s.commit()

    async def add_dir(self, user_id: int, name: str, path: str) -> None:
        async with self.sf() as s:
            s.add(DownloadDir(user_id=user_id, name=name, path=path))
            await s.commit()

    async def user_dirs(self, user_id: int) -> list[DownloadDir]:
        async with self.sf() as s:
            rows = await s.scalars(select(DownloadDir).where(DownloadDir.user_id == user_id))
            return list(rows)

    async def history(self, user_id: int, page: int, page_size: int) -> tuple[list[Torrent], int]:
        async with self.sf() as s:
            total = int((await s.execute(select(func.count()).select_from(Torrent).where(Torrent.user_id == user_id))).scalar_one())
            rows = await s.scalars(select(Torrent).where(Torrent.user_id == user_id).order_by(Torrent.added_at.desc()).offset((page-1)*page_size).limit(page_size))
            return list(rows), total
