# Copyright (c) 2026 Any1Key
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.i18n import t


def history_kb(page: int, total_pages: int, lang: str) -> InlineKeyboardMarkup:
    row=[]
    if page>1: row.append(InlineKeyboardButton(text=t("btn.back", lang), callback_data=f"history:{page-1}"))
    row.append(InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data=f"history:{page}"))
    if page<total_pages: row.append(InlineKeyboardButton(text=t("btn.forward", lang), callback_data=f"history:{page+1}"))
    return InlineKeyboardMarkup(inline_keyboard=[row, [InlineKeyboardButton(text=t("btn.main_menu", lang), callback_data="menu")]])
