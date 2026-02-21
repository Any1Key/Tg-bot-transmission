from __future__ import annotations

import asyncio
from pathlib import Path

from transmission_rpc import Client


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
            t = self._c().add_torrent(str(file_path), paused=True)
            return str(t.hashString), str(t.name)
        return await asyncio.to_thread(_run)

    async def set_dir_and_start(self, torrent_hash: str, download_dir: str) -> None:
        def _run() -> None:
            c = self._c()
            c.change_torrent([torrent_hash], download_dir=download_dir)
            c.start_torrent([torrent_hash])
        await asyncio.to_thread(_run)

    async def torrent(self, torrent_hash: str):
        return await asyncio.to_thread(lambda: self._c().get_torrent(torrent_hash))

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

    async def stats(self) -> dict[str, int]:
        def _run() -> dict[str, int]:
            s = self._c().session_stats()
            c = getattr(s, "cumulative_stats", None)
            return {
                "downloaded": int(getattr(c, "downloadedBytes", 0) if c else 0),
                "uploaded": int(getattr(c, "uploadedBytes", 0) if c else 0),
                "download_speed": int(getattr(s, "downloadSpeed", 0) or 0),
                "upload_speed": int(getattr(s, "uploadSpeed", 0) or 0),
                "active": int(getattr(s, "activeTorrentCount", 0) or 0),
            }
        return await asyncio.to_thread(_run)
