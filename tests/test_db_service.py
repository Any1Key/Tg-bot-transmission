# Copyright (c) 2026 Any1Key
from __future__ import annotations

import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.models.base import Base
from bot.models.torrent import Torrent
from bot.services.db import DBService


class DBServiceTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.tmp_dir = tempfile.TemporaryDirectory()
        db_path = Path(self.tmp_dir.name) / "test.db"
        self.engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}", echo=False)
        self.sf = async_sessionmaker(self.engine, expire_on_commit=False)
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        self.db = DBService(self.sf)

    async def asyncTearDown(self) -> None:
        await self.engine.dispose()
        self.tmp_dir.cleanup()

    async def test_cleanup_missing_removes_records(self) -> None:
        await self.db.add_torrent(1, "hash-a", "Torrent A")
        await self.db.mark_missing("hash-a")

        removed = await self.db.cleanup_missing()

        self.assertEqual(removed, 1)
        async with self.sf() as s:
            rows = await s.scalars(select(Torrent))
            self.assertEqual(list(rows), [])

    async def test_cleanup_stale_pending_removes_only_old_records(self) -> None:
        await self.db.add_torrent(1, "hash-old", "Old pending")
        await self.db.add_torrent(1, "hash-new", "New pending")

        old_dt = datetime.now(timezone.utc) - timedelta(hours=48)
        async with self.sf() as s:
            await s.execute(
                update(Torrent)
                .where(Torrent.torrent_hash == "hash-old")
                .values(added_at=old_dt)
            )
            await s.commit()

        removed = await self.db.cleanup_stale_pending(24)
        self.assertEqual(removed, 1)

        async with self.sf() as s:
            hashes = list(await s.scalars(select(Torrent.torrent_hash)))
            self.assertEqual(hashes, ["hash-new"])


if __name__ == "__main__":
    unittest.main()
