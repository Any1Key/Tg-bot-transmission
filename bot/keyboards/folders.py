# Copyright (c) 2026 Any1Key
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def dir_kb(torrent_hash: str, dirs: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=f"📁 Выбрать: {name}", callback_data=f"pick:{torrent_hash}:{i}")] for i, (name, _) in enumerate(dirs)]
    rows.append([InlineKeyboardButton(text="🏠 В главное меню", callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def folders_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 В главное меню", callback_data="menu")]])
