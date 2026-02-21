from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏸️ Приостановить все", callback_data="admin:pause"), InlineKeyboardButton(text="▶️ Возобновить все", callback_data="admin:resume")],
        [InlineKeyboardButton(text="🔄 Перезапустить Transmission", callback_data="admin:restart")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="stats"), InlineKeyboardButton(text="📁 Папки", callback_data="folders")],
        [InlineKeyboardButton(text="📜 История", callback_data="history:1")],
    ])
