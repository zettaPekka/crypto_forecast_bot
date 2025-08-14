from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ContentType, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from forecast_bot.middlewares.db_di import DatabaseDI
from database.services.user_service import UserService
from database.services.trader_data_service import TraderDataService
from database.services.stat_service import StatService
from forecast_bot.states.user_states import UserDataState
from forecast_bot.keyboards import user_kbs
from parse.news_parser import get_current_news

from random import randint
from datetime import datetime, timezone, timedelta


router = Router()
router.message.middleware(DatabaseDI())
router.callback_query.middleware(DatabaseDI())

@router.callback_query(F.data == 'forecast_menu')
async def forecast_menu(callback: CallbackQuery, user_service: UserService):
    await callback.answer()
    
    try:
        await callback.message.delete()
    except:
        pass
    
    user = await user_service.get(callback.from_user.id)
    
    await callback.message.answer('Меню',
                                    reply_markup=user_kbs.forecast_menu(user.otc))


@router.callback_query(F.data.startswith('currency_pairs'))
async def currency_pairs(callback: CallbackQuery, user_service: UserService):
    await callback.answer()
    
    user = await user_service.get(callback.from_user.id)
    
    if len(callback.data.split('_')) < 3: # страница не указана
        await callback.message.edit_text('выберите пару',
                                    reply_markup=user_kbs.currency_pairs_by_page(user.otc, 1))
        return
    
    page = int(callback.data.split('_')[-1])
    await callback.message.edit_text('выберите пару',
                                    reply_markup=user_kbs.currency_pairs_by_page(user.otc, page))


@router.callback_query(F.data.startswith('currency_pairs'))
async def currency_pairs(callback: CallbackQuery, user_service: UserService):
    await callback.answer()
    
    user = await user_service.get(callback.from_user.id)
    
    if len(callback.data.split('_')) < 3: # страница не указана
        await callback.message.edit_text('выберите пару',
                                    reply_markup=user_kbs.currency_pairs_by_page(user.otc, 1))
        return
    
    page = int(callback.data.split('_')[-1])
    await callback.message.edit_text('выберите пару',
                                    reply_markup=user_kbs.currency_pairs_by_page(user.otc, page))
