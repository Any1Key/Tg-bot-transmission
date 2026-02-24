# Copyright (c) 2026 Any1Key
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.i18n import t


def folder_icon(name: str, path: str) -> str:
    blob = f"{name} {path}".lower()
    rules = [
        (("film", "movie", "кино", "фильм"), "🎬"),
        (("serial", "series", "сериал"), "📺"),
        (("music", "audio", "музык"), "🎵"),
        (("book", "ebook", "книг"), "📚"),
        (("anime", "аниме"), "🌸"),
        (("game", "игр"), "🎮"),
        (("photo", "image", "фото"), "🖼️"),
        (("doc", "document", "док"), "📄"),
        (("other", "misc", "другое"), "📦"),
    ]
    for keys, icon in rules:
        if any(k in blob for k in keys):
            return icon
    fallback = ["🗂️", "📁", "🧰", "🗃️", "📦"]
    idx = sum(ord(ch) for ch in blob) % len(fallback)
    return fallback[idx]


def dir_kb(torrent_hash: str, dirs: list[tuple[str, str]], lang: str) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                text=f"{folder_icon(name, path)} {t('btn.pick', lang, name=name)}",
                callback_data=f"pick:{torrent_hash}:{i}",
            )
        ]
        for i, (name, path) in enumerate(dirs)
    ]
    rows.append([InlineKeyboardButton(text=t("btn.main_menu", lang), callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def folders_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=t("btn.main_menu", lang), callback_data="menu")]])
