# Copyright (c) 2026 Any1Key
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.i18n import t


def language_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:set:ru")],
            [InlineKeyboardButton(text="🇺🇸 English", callback_data="lang:set:en")],
            [InlineKeyboardButton(text=t("btn.main_menu", lang), callback_data="menu")],
        ]
    )
