# Copyright (c) 2026 Any1Key
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def _short(name: str, max_len: int = 28) -> str:
    if len(name) <= max_len:
        return name
    return name[: max_len - 1] + "…"


def incomplete_kb(items: list[dict[str, object]]) -> InlineKeyboardMarkup:
    rows = []
    for item in items[:15]:
        torrent_hash = str(item["hash"])
        name = _short(str(item["name"]))
        progress = int(item["progress"])
        rows.append([InlineKeyboardButton(text=f"▶️ Продолжить: {name} ({progress}%)", callback_data=f"incomplete:resume:{torrent_hash}")])

    if items:
        rows.append([InlineKeyboardButton(text="▶️ Продолжить все недокачанные", callback_data="incomplete:resume_all")])
    rows.append([InlineKeyboardButton(text="🔄 Обновить список", callback_data="incomplete:refresh")])
    rows.append([InlineKeyboardButton(text="🏠 В главное меню", callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
