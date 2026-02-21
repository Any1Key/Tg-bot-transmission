# Copyright (c) 2026 Any1Key
from __future__ import annotations

import asyncio
import logging

from aiogram import Bot

from bot.services.db import DBService
from bot.services.transmission import TransmissionService
from bot.utils.formatters import human
from bot.utils.markdown import esc


class Monitor:
    def __init__(self, db: DBService, tx: TransmissionService, bot: Bot, interval: int) -> None:
        self.db=db; self.tx=tx; self.bot=bot; self.interval=interval; self.task: asyncio.Task|None=None

    def start(self) -> None:
        self.task = asyncio.create_task(self.run())

    async def stop(self) -> None:
        if self.task:
            self.task.cancel()

    async def run(self) -> None:
        while True:
            try:
                for item in await self.db.get_pending():
                    t = await self.tx.torrent(item.torrent_hash)
                    done = float(getattr(t, "percentDone", 0.0) or 0.0) >= 1.0
                    status = str(getattr(t, "status", "")).lower()
                    if done and ("seed" in status or "stop" in status):
                        ratio = float(getattr(t, "uploadRatio", 0.0) or 0.0)
                        size = int(getattr(t, "totalSize", 0) or 0)
                        await self.db.complete(item.torrent_hash, ratio, size, None)
                        await self.bot.send_message(item.user_id, f"✅ *Завершено*\n📦 *{esc(item.torrent_name)}*\n📏 {esc(human(size))}\n🔁 {ratio:.2f}")
            except Exception:
                logging.exception("monitor iteration failed")
            await asyncio.sleep(self.interval)
