# Copyright (c) 2026 Any1Key
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def stats_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Обновить статистику", callback_data="stats")],
            [InlineKeyboardButton(text="🏠 В главное меню", callback_data="menu")],
        ]
    )
