# Copyright (c) 2026 Any1Key
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.i18n import t


def dir_kb(torrent_hash: str, dirs: list[tuple[str, str]], lang: str) -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=t("btn.pick", lang, name=name), callback_data=f"pick:{torrent_hash}:{i}")] for i, (name, _) in enumerate(dirs)]
    rows.append([InlineKeyboardButton(text=t("btn.main_menu", lang), callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def folders_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=t("btn.main_menu", lang), callback_data="menu")]])
