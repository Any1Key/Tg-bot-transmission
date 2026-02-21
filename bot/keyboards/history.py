# Copyright (c) 2026 Any1Key
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def history_kb(page: int, total_pages: int) -> InlineKeyboardMarkup:
    row=[]
    if page>1: row.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"history:{page-1}"))
    row.append(InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data=f"history:{page}"))
    if page<total_pages: row.append(InlineKeyboardButton(text="Вперёд ➡️", callback_data=f"history:{page+1}"))
    return InlineKeyboardMarkup(inline_keyboard=[row, [InlineKeyboardButton(text="🏠 В главное меню", callback_data="menu")]])
