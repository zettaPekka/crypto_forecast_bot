from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

import math

from config import *


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

reg_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🚀 Создать аккаунт', url='https://u3.shortink.io/pwa?utm_campaign=825395&utm_source=affiliate&utm_medium=sr&a=e0yBQmescshMRL&ac=j1ko')]
])

start_left_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔓 Получить доступ', callback_data='get_access'),
        InlineKeyboardButton(text='🆘 Помощь', url='https://t.me/jiko_trade')]
])

check_dep_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔍 Проверить депозит', callback_data='check_dep')]
])

main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🎯 Получить прогноз', callback_data='forecast_menu')],
    [InlineKeyboardButton(text='📰 Новости', callback_data='news')],
    [InlineKeyboardButton(text='🎁 Промокоды', callback_data='promo')],
    [InlineKeyboardButton(text='📊 Статистика', callback_data='statistics')],
    [InlineKeyboardButton(text='🎓 Обучение', url='https://dsfsfsdf.re')]
])


def forecast_menu(otc: bool):
    otc_status = '✅ OTC ВКЛ' if otc else '❌ OTC ВЫКЛ'
    
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=otc_status, callback_data='change_otc'),
            InlineKeyboardButton(text='🏠 Меню', callback_data='menu')],
        [InlineKeyboardButton(text='💱 Валютные пары', callback_data='currency_pairs')],
        [InlineKeyboardButton(text='🪙 Криптовалюта', callback_data='crypto')],
        [InlineKeyboardButton(text='📈 Индексы', callback_data='indices')],
        [InlineKeyboardButton(text='📦 Сырьевые товары', callback_data='commodities')],
        [InlineKeyboardButton(text='💼 Акции', callback_data='stocks')]
    ])

def currency_pairs_by_page(otc: bool, page: int):
    otc = 'OTC' if otc else ''
    
    builder = InlineKeyboardBuilder()
    
    for pair in pairs[(page - 1) * 10: page * 10]:
        builder.add(InlineKeyboardButton(text=f'{pair} {otc}', callback_data=f'get_forecast_{pair}'))
    
    if page == 1:
        builder.add(InlineKeyboardButton(text='👉', callback_data=f'currency_pairs_page_{page + 1}'))
    elif page >= math.ceil(len(pairs) // 10):
        builder.add(InlineKeyboardButton(text=f'👈', callback_data=f'currency_pairs_page_{page - 1}'))
    else:
        builder.add(InlineKeyboardButton(text=f'👈', callback_data=f'currency_pairs_page_{page - 1}'))
        builder.add(InlineKeyboardButton(text='👉', callback_data=f'currency_pairs_page_{page + 1}'))
    
    builder.add(InlineKeyboardButton(text=f'🔙 Обратно', callback_data='forecast_menu'))
    
    builder.adjust(2)
    return builder.as_markup()


def crypto_by_page(otc: bool, page: int):
    otc = 'OTC' if otc else ''
    
    builder = InlineKeyboardBuilder()
    
    for c in crypto[(page - 1) * 10: page * 10]:
        builder.add(InlineKeyboardButton(text=f'{c} {otc}', callback_data=f'get_forecast_{c}'))
    
    if page == 1:
        builder.add(InlineKeyboardButton(text='👉', callback_data=f'crypto_page_{page + 1}'))
    elif page >= math.ceil(len(crypto) / 10):
        builder.add(InlineKeyboardButton(text=f'👈', callback_data=f'crypto_page_{page - 1}'))
    else:
        builder.add(InlineKeyboardButton(text=f'👈', callback_data=f'crypto_page_{page - 1}'))
        builder.add(InlineKeyboardButton(text='👉', callback_data=f'crypto_page_{page + 1}'))
    
    builder.add(InlineKeyboardButton(text=f'🔙 Обратно', callback_data='forecast_menu'))
    
    builder.adjust(2)
    return builder.as_markup()


def indices_by_page(otc: bool, page: int):
    otc = 'OTC' if otc else ''
    
    builder = InlineKeyboardBuilder()
    
    for i in indices[(page - 1) * 10: page * 10]:
        builder.add(InlineKeyboardButton(text=f'{i} {otc}', callback_data=f'get_forecast_{i}'))
    
    if page == 1:
        builder.add(InlineKeyboardButton(text='👉', callback_data=f'indices_page_{page + 1}'))
    elif page >= math.ceil(len(indices) / 10):
        builder.add(InlineKeyboardButton(text=f'👈', callback_data=f'indices_page_{page - 1}'))
    else:
        builder.add(InlineKeyboardButton(text=f'👈', callback_data=f'indices_page_{page - 1}'))
        builder.add(InlineKeyboardButton(text='👉', callback_data=f'indices_page_{page + 1}'))
    
    builder.add(InlineKeyboardButton(text=f'🔙 Обратно', callback_data='forecast_menu'))
    
    builder.adjust(2)
    return builder.as_markup()


def commodities_by_page(otc: bool, page: int):
    otc = 'OTC' if otc else ''
    
    builder = InlineKeyboardBuilder()
    
    for c in commodities[(page - 1) * 10: page * 10]:
        builder.add(InlineKeyboardButton(text=f'{c} {otc}', callback_data=f'get_forecast_{c}'))
    
    if page == 1:
        builder.add(InlineKeyboardButton(text='👉', callback_data=f'commodities_page_{page + 1}'))
    elif page >= math.ceil(len(commodities) / 10):
        builder.add(InlineKeyboardButton(text=f'👈', callback_data=f'commodities_page_{page - 1}'))
    else:
        builder.add(InlineKeyboardButton(text=f'👈', callback_data=f'commodities_page_{page - 1}'))
        builder.add(InlineKeyboardButton(text='👉', callback_data=f'commodities_page_{page + 1}'))
    
    builder.add(InlineKeyboardButton(text=f'🔙 Обратно', callback_data='forecast_menu'))
    
    builder.adjust(2)
    return builder.as_markup()


def stocks_by_page(otc: bool, page: int):
    otc = 'OTC' if otc else ''
    
    builder = InlineKeyboardBuilder()
    
    for s in stocks[(page - 1) * 10: page * 10]:
        builder.add(InlineKeyboardButton(text=f'{s} {otc}', callback_data=f'get_forecast_{s}'))
    
    if page == 1:
        builder.add(InlineKeyboardButton(text='👉', callback_data=f'stocks_page_{page + 1}'))
    elif page >= math.ceil(len(stocks) / 10):
        builder.add(InlineKeyboardButton(text=f'👈', callback_data=f'stocks_page_{page - 1}'))
    else:
        builder.add(InlineKeyboardButton(text=f'👈', callback_data=f'stocks_page_{page - 1}'))
        builder.add(InlineKeyboardButton(text='👉', callback_data=f'stocks_page_{page + 1}'))
    
    builder.add(InlineKeyboardButton(text=f'🔙 Обратно', callback_data='forecast_menu'))
    
    builder.adjust(2)
    return builder.as_markup()


period = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='15s', callback_data='period_15s'),
            InlineKeyboardButton(text='30s', callback_data='period_30s')],
        [InlineKeyboardButton(text='1m', callback_data='period_1m'),
            InlineKeyboardButton(text='2m', callback_data='period_2m')],
        [InlineKeyboardButton(text='3m', callback_data='period_3m'),
            InlineKeyboardButton(text='5m', callback_data='period_5m')],
        [InlineKeyboardButton(text='10m', callback_data='period_10m'),
            InlineKeyboardButton(text='15m', callback_data='period_15m')],
        [InlineKeyboardButton(text='30m', callback_data='period_30m'),
            InlineKeyboardButton(text='60m', callback_data='period_60m')]
    ]
)