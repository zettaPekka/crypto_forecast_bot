from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start_left_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Получить доступ', callback_data='get_access'),
    InlineKeyboardButton(text='Помощь', url='https://fdfsffff.ru')]
])

check_dep_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Проверить депозит', callback_data='check_dep')]
])