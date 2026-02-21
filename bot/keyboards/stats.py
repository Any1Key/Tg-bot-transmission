from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def stats_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔄 Обновить", callback_data="stats")], [InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu")]])
