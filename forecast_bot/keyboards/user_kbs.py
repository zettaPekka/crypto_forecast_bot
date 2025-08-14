from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.database import get_session
from database.repositories.user_repo import UserRepo
from database.services.user_service import UserService

from config import pairs



start_left_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Получить доступ', callback_data='get_access'),
    InlineKeyboardButton(text='Помощь', url='https://fdfsffff.ru')]
])

check_dep_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Проверить депозит', callback_data='check_dep')]
])

main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Получить прогноз', callback_data='forecast_menu')],
    [InlineKeyboardButton(text='Новости', callback_data='news')],
    [InlineKeyboardButton(text='Промокоды', callback_data='promo')],
    [InlineKeyboardButton(text='Статистика', callback_data='statistics')],
    [InlineKeyboardButton(text='Обучение', callback_data='learning')]
])

def forecast_menu(otc: bool):
    otc = 'OTC ✅' if otc else 'OTC ❌'
    
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=otc, callback_data='change_otc'),
            InlineKeyboardButton(text='Обратно', callback_data='menu')],
        [InlineKeyboardButton(text='Валютные пары', callback_data='currency_pairs')],
        [InlineKeyboardButton(text='Криптовалюта', callback_data='crypto')],
        [InlineKeyboardButton(text='Индексы', callback_data='indecies')],
        [InlineKeyboardButton(text='Сырьевые товары', callback_data='commodities')],
        [InlineKeyboardButton(text='Акции', callback_data='stocks')]
    ])

def currency_pairs_by_page(otc: bool, page: int):
    otc = 'OTC' if otc else ''
    
    builder = InlineKeyboardBuilder()
    
    for pair in pairs[(page - 1) * 10: page * 10]:
        builder.add(InlineKeyboardButton(text=f'{pair} {otc}', callback_data=f'get_forecast_{pair}'))
    
    if page == 1:
        builder.add(InlineKeyboardButton(text='👉', callback_data=f'currency_pairs_page_{page + 1}'))
    elif page > len(pairs) // 10:
        builder.add(InlineKeyboardButton(text=f'👈', callback_data=f'currency_pairs_page_{page - 1}'))
    else:
        builder.add(InlineKeyboardButton(text='👉', callback_data=f'currency_pairs_page_{page + 1}'))
        builder.add(InlineKeyboardButton(text=f'👈', callback_data=f'currency_pairs_page_{page - 1}'))
    
    builder.add(InlineKeyboardButton(text=f'Меню', callback_data='menu'))
    
    builder.adjust(2)
    return builder.as_markup()