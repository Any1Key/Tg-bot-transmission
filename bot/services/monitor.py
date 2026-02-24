# Copyright (c) 2026 Any1Key
from __future__ import annotations

import asyncio
import logging

from aiogram import Bot

from bot.services.db import DBService
from bot.services.transmission import TorrentNotFoundError, TransmissionService
from bot.utils.formatters import human
from bot.utils.markdown import esc


def _pick_float(obj: object, *names: str) -> float | None:
    for name in names:
        val = getattr(obj, name, None)
        if val is not None:
            try:
                return float(val)
            except (TypeError, ValueError):
                continue
    fields = getattr(obj, "fields", {}) or {}
    for name in names:
        if name in fields and fields[name] is not None:
            try:
                return float(fields[name])
            except (TypeError, ValueError):
                continue
    return None


def _pick_int(obj: object, *names: str) -> int | None:
    for name in names:
        val = getattr(obj, name, None)
        if val is not None:
            try:
                return int(val)
            except (TypeError, ValueError):
                continue
    fields = getattr(obj, "fields", {}) or {}
    for name in names:
        if name in fields and fields[name] is not None:
            try:
                return int(fields[name])
            except (TypeError, ValueError):
                continue
    return None


def _pick_bool(obj: object, *names: str) -> bool | None:
    for name in names:
        val = getattr(obj, name, None)
        if val is not None:
            return bool(val)
    fields = getattr(obj, "fields", {}) or {}
    for name in names:
        if name in fields and fields[name] is not None:
            return bool(fields[name])
    return None


def _is_complete(obj: object) -> bool:
    progress = _pick_float(obj, "percentDone", "percent_done")
    left = _pick_int(obj, "leftUntilDone", "left_until_done")
    is_finished = _pick_bool(obj, "isFinished", "is_finished")
    return bool((progress is not None and progress >= 1.0) or (left is not None and left <= 0) or is_finished)


class Monitor:
    def __init__(self, db: DBService, tx: TransmissionService, bot: Bot, interval: int) -> None:
        self.db=db; self.tx=tx; self.bot=bot; self.interval=interval; self.task: asyncio.Task|None=None

    def start(self) -> None:
        self.task = asyncio.create_task(self.run())

    async def stop(self) -> None:
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass

    async def run(self) -> None:
        while True:
            try:
                for item in await self.db.get_pending():
                    try:
                        t = await self.tx.torrent(item.torrent_hash)
                    except TorrentNotFoundError:
                        logging.warning("monitor: torrent missing in transmission, hash=%s", item.torrent_hash)
                        await self.db.mark_missing(item.torrent_hash)
                        continue
                    except Exception:
                        logging.exception("monitor: failed to fetch torrent, hash=%s", item.torrent_hash)
                        continue

                    if _is_complete(t):
                        ratio = _pick_float(t, "uploadRatio", "upload_ratio") or 0.0
                        size = _pick_int(t, "totalSize", "total_size") or 0
                        await self.db.complete(item.torrent_hash, ratio, size, None)
                        lang = await self.db.ensure_user_lang(item.user_id, None)
                        done_title = "✅ *Завершено*" if lang == "ru" else "✅ *Completed*"
                        size_title = "📏 Размер" if lang == "ru" else "📏 Size"
                        ratio_title = "🔁 Рейтинг" if lang == "ru" else "🔁 Ratio"
                        await self.bot.send_message(
                            item.user_id,
                            f"{done_title}\n📦 *{esc(item.torrent_name)}*\n{size_title}: {esc(human(size))}\n{ratio_title}: {ratio:.2f}",
                        )
            except Exception:
                logging.exception("monitor iteration failed")
            await asyncio.sleep(self.interval)
