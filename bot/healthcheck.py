# Copyright (c) 2026 Any1Key
from __future__ import annotations

from bot.config import Settings
from transmission_rpc import Client


def main() -> int:
    try:
        s = Settings()
        c = s.transmission_conn
        client = Client(
            protocol=c["protocol"],
            host=c["host"],
            port=int(c["port"]),
            path=str(c["path"]),
            username=s.transmission_user,
            password=s.transmission_pass,
            timeout=10,
        )
        client.session_stats()
        return 0
    except Exception:
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
