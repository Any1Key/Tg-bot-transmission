# Copyright (c) 2026 Any1Key
from __future__ import annotations

import asyncio
from pathlib import Path

from transmission_rpc import Client


class TorrentNotFoundError(Exception):
    pass


class TransmissionService:
    def __init__(self, conn: dict[str, object], username: str, password: str) -> None:
        self.conn = conn
        self.username = username
        self.password = password

    def _c(self) -> Client:
        return Client(protocol=self.conn["protocol"], host=self.conn["host"], port=int(self.conn["port"]), path=str(self.conn["path"]), username=self.username, password=self.password, timeout=15)

    async def add_magnet(self, magnet: str) -> tuple[str, str]:
        def _run() -> tuple[str, str]:
            t = self._c().add_torrent(magnet, paused=True)
            return str(t.hashString), str(t.name)
        return await asyncio.to_thread(_run)

    async def add_file(self, file_path: Path) -> tuple[str, str]:
        def _run() -> tuple[str, str]:
            c = self._c()
            # Для transmission-rpc 4.x локальные файлы лучше передавать Path/bytes,
            # строковый путь может интерпретироваться не как локальный торрент.
            try:
                t = c.add_torrent(file_path, paused=True)
            except Exception:
                data = file_path.read_bytes()
                t = c.add_torrent(data, paused=True)
            return str(t.hashString), str(t.name)
        return await asyncio.to_thread(_run)

    async def set_dir_and_start(self, torrent_hash: str, download_dir: str) -> None:
        def _run() -> None:
            c = self._c()
            # Устанавливаем целевой путь торрента через torrent-set-location.
            # move=False: не переносим текущие данные вручную, Transmission сам
            # использует incomplete dir и перенесет готовый торрент в location.
            c.move_torrent_data([torrent_hash], download_dir, move=False)
            c.start_torrent([torrent_hash])
        await asyncio.to_thread(_run)

    async def torrent(self, torrent_hash: str):
        def _run():
            try:
                return self._c().get_torrent(torrent_hash)
            except KeyError as exc:
                if "Torrent not found" in str(exc):
                    raise TorrentNotFoundError(torrent_hash) from exc
                raise

        return await asyncio.to_thread(_run)

    async def pause_all(self) -> int:
        def _run() -> int:
            c=self._c(); ts=c.get_torrents(); ids=[t.id for t in ts]
            if ids: c.stop_torrent(ids)
            return len(ids)
        return await asyncio.to_thread(_run)

    async def resume_all(self) -> int:
        def _run() -> int:
            c=self._c(); ts=c.get_torrents(); ids=[t.id for t in ts]
            if ids: c.start_torrent(ids)
            return len(ids)
        return await asyncio.to_thread(_run)

    async def resume_one(self, torrent_hash: str) -> None:
        def _run() -> None:
            c = self._c()
            c.start_torrent([torrent_hash])
        await asyncio.to_thread(_run)

    async def incomplete(self) -> list[dict[str, object]]:
        def _run() -> list[dict[str, object]]:
            def pick_float(obj: object, *names: str) -> float | None:
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

            def pick_int(obj: object, *names: str) -> int | None:
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

            def pick_bool(obj: object, *names: str) -> bool | None:
                for name in names:
                    val = getattr(obj, name, None)
                    if val is not None:
                        return bool(val)
                fields = getattr(obj, "fields", {}) or {}
                for name in names:
                    if name in fields and fields[name] is not None:
                        return bool(fields[name])
                return None

            out: list[dict[str, object]] = []
            for t in self._c().get_torrents():
                progress = pick_float(t, "percentDone", "percent_done")
                left = pick_int(t, "leftUntilDone", "left_until_done")
                is_finished = pick_bool(t, "isFinished", "is_finished")
                if (progress is not None and progress >= 1.0) or (left is not None and left <= 0) or bool(is_finished):
                    continue
                status = str(getattr(t, "status", "") or "")
                progress_pct = int((progress or 0.0) * 100)
                out.append(
                    {
                        "hash": str(getattr(t, "hashString", "")),
                        "name": str(getattr(t, "name", "unknown")),
                        "status": status,
                        "progress": progress_pct,
                    }
                )
            return out

        return await asyncio.to_thread(_run)

    async def stats(self) -> dict[str, int]:
        def _run() -> dict[str, int]:
            s = self._c().session_stats()
            c = getattr(s, "cumulative_stats", None)

            def pick(obj, *names: str, default: int = 0) -> int:
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
                return default

            return {
                "downloaded": pick(c, "downloaded_bytes", "downloadedBytes") if c else 0,
                "uploaded": pick(c, "uploaded_bytes", "uploadedBytes") if c else 0,
                "download_speed": pick(s, "download_speed", "downloadSpeed"),
                "upload_speed": pick(s, "upload_speed", "uploadSpeed"),
                "active": pick(s, "active_torrent_count", "activeTorrentCount"),
            }
        return await asyncio.to_thread(_run)
