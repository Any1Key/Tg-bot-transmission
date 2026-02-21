from __future__ import annotations

from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject


class AuthMiddleware(BaseMiddleware):
    def __init__(self, allowed: set[int]) -> None:
        self.allowed = allowed

    async def __call__(self, handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: dict[str, Any]) -> Any:
        user_id = None
        if isinstance(event, Message) and event.from_user: user_id = event.from_user.id
        if isinstance(event, CallbackQuery) and event.from_user: user_id = event.from_user.id
        if user_id not in self.allowed:
            if isinstance(event, Message): await event.answer("⛔ Доступ запрещен")
            elif isinstance(event, CallbackQuery): await event.answer("⛔ Доступ запрещен", show_alert=True)
            return None
        return await handler(event, data)
