from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def history_kb(page: int, total_pages: int) -> InlineKeyboardMarkup:
    row=[]
    if page>1: row.append(InlineKeyboardButton(text="←", callback_data=f"history:{page-1}"))
    row.append(InlineKeyboardButton(text=str(page), callback_data=f"history:{page}"))
    if page<total_pages: row.append(InlineKeyboardButton(text="→", callback_data=f"history:{page+1}"))
    return InlineKeyboardMarkup(inline_keyboard=[row, [InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu")]])
