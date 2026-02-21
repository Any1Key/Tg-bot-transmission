# Copyright (c) 2026 Any1Key
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Статистика сети"), KeyboardButton(text="🗂️ Системные папки")],
            [KeyboardButton(text="📜 История загрузок"), KeyboardButton(text="⬇️ Недокачанные торренты")],
            [KeyboardButton(text="⏸️ Пауза всех торрентов"), KeyboardButton(text="▶️ Продолжить все торренты")],
            [KeyboardButton(text="🏠 Открыть главное меню")],
        ],
        resize_keyboard=True,
    )
