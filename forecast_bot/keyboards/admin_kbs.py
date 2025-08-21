from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


send_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сделать рассылку', callback_data='sending')]
])

back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='cancel')]
])