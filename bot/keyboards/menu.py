# Copyright (c) 2026 Any1Key
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.i18n import t


def menu_kb(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("btn.stats", lang)), KeyboardButton(text=t("btn.folders", lang))],
            [KeyboardButton(text=t("btn.history", lang)), KeyboardButton(text=t("btn.incomplete", lang))],
            [KeyboardButton(text=t("btn.pause_all", lang)), KeyboardButton(text=t("btn.resume_all", lang))],
            [KeyboardButton(text=t("btn.language", lang)), KeyboardButton(text=t("btn.open_menu", lang))],
        ],
        resize_keyboard=True,
    )
