from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def dir_kb(torrent_hash: str, dirs: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=f"📁 {name}", callback_data=f"pick:{torrent_hash}:{i}")] for i, (name, _) in enumerate(dirs)]
    rows.append([InlineKeyboardButton(text="➕ Добавить свою папку", callback_data=f"adddir:{torrent_hash}")])
    rows.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
