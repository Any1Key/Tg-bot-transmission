# Copyright (c) 2026 Any1Key
from __future__ import annotations

import time
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject


class ThrottleMiddleware(BaseMiddleware):
    def __init__(self, sec: float) -> None:
        self.sec = sec
        self.last: dict[int, float] = {}

    async def __call__(self, handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: dict[str, Any]) -> Any:
        uid = None
        if isinstance(event, Message) and event.from_user: uid = event.from_user.id
        if isinstance(event, CallbackQuery) and event.from_user: uid = event.from_user.id
        if uid is not None:
            now = time.monotonic()
            if now - self.last.get(uid, 0) < self.sec:
                if isinstance(event, Message): await event.answer("⏳ Подождите")
                elif isinstance(event, CallbackQuery): await event.answer("⏳")
                return None
            self.last[uid] = now
        return await handler(event, data)
