# Copyright (c) 2026 Any1Key
from __future__ import annotations

import unittest
from unittest.mock import Mock

from bot.services.transmission import TorrentNotFoundError, TransmissionService


class TransmissionServiceTest(unittest.IsolatedAsyncioTestCase):
    async def test_torrent_maps_not_found_keyerror(self) -> None:
        svc = TransmissionService(
            conn={"protocol": "http", "host": "localhost", "port": 9091, "path": "/transmission/rpc"},
            username="u",
            password="p",
        )
        fake_client = Mock()
        fake_client.get_torrent.side_effect = KeyError("Torrent not found in result")
        svc._c = lambda: fake_client  # type: ignore[method-assign]

        with self.assertRaises(TorrentNotFoundError):
            await svc.torrent("abc")

    async def test_torrent_keeps_other_keyerrors(self) -> None:
        svc = TransmissionService(
            conn={"protocol": "http", "host": "localhost", "port": 9091, "path": "/transmission/rpc"},
            username="u",
            password="p",
        )
        fake_client = Mock()
        fake_client.get_torrent.side_effect = KeyError("Some other key error")
        svc._c = lambda: fake_client  # type: ignore[method-assign]

        with self.assertRaises(KeyError):
            await svc.torrent("abc")


if __name__ == "__main__":
    unittest.main()
