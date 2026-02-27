# Copyright (c) 2026 Any1Key
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.i18n import t

def _short(name: str, max_len: int = 22) -> str:
    if len(name) <= max_len:
        return name
    return name[: max_len - 1] + "…"


def incomplete_kb(items: list[dict[str, object]], lang: str) -> InlineKeyboardMarkup:
    rows = []
    for item in items[:15]:
        torrent_hash = str(item["hash"])
        name = _short(str(item["name"]))
        progress = int(item["progress"])
        rows.append([InlineKeyboardButton(text=t("btn.resume", lang, name=name, progress=progress), callback_data=f"incomplete:resume:{torrent_hash}")])

    if items:
        rows.append([InlineKeyboardButton(text=t("btn.resume_incomplete_all", lang), callback_data="incomplete:resume_all")])
    rows.append([InlineKeyboardButton(text=t("btn.refresh_list", lang), callback_data="incomplete:refresh")])
    rows.append([InlineKeyboardButton(text=t("btn.main_menu", lang), callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
