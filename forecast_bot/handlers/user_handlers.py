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


@router.message(CommandStart())
async def start_handler(message: Message, user_service: UserService, trader_data_service: TraderDataService):
    tg_id = message.from_user.id
    
    await user_service.create_if_not_exists(tg_id)
    trader_data = await trader_data_service.get_by_tg_id(tg_id)
    
    if not trader_data:
        image = FSInputFile('images/photo.jpg')
        await message.answer_photo(image, caption='Вы еще не зарегестрированы, нажмите кнопку далее чтобы получить доступ',
                                reply_markup=user_kbs.start_left_kb)
        return

    if trader_data.balance > 0:
        image = FSInputFile('images/photo.jpg')
        await message.answer_photo(image, caption='Вы уже зарегестрированы и у вас есть доступ к функциям',
                                    reply_markup=user_kbs.main_kb)
        return
    
    image = FSInputFile('images/photo.jpg')
    await message.answer_photo(image, caption='Вы зарегестрированы, пополните баланс на любую сумму и нажмите кнопку ниже чтобы проверить депозит',
                            reply_markup=user_kbs.check_dep_kb)


@router.callback_query(F.data == 'get_access')
async def get_access(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    image = FSInputFile('images/photo.jpg')
    image = InputMediaPhoto(media=image, caption='скинь id')
    await callback.message.edit_media(image)
    await state.set_state(UserDataState.trader_id)


@router.message(UserDataState.trader_id)
async def check_trader_id(message: Message, trader_data_service: TraderDataService, state: FSMContext):
    trader_id = int(message.text) if message.text.isdigit() else -1
    res = await trader_data_service.check_trader_id(trader_id, message.from_user.id)
    
    if res:
        await message.answer('привязано, теперь пополни баланс и проверь по кнопке ниже',
                                reply_markup=user_kbs.check_dep_kb)
        await state.clear()
        return
    
    await message.answer('не тот id')


@router.callback_query(F.data == 'check_dep')
async def check_dep(callback: CallbackQuery, trader_data_service: TraderDataService):
    await callback.answer()
    
    trader_data = await trader_data_service.get_by_tg_id(callback.from_user.id)
    
    if trader_data.balance > 0:
        image = FSInputFile('images/photo.jpg')
        await callback.message.answer_photo(image, caption='успешно, у вас есть доступ к функциям',
                                            reply_markup=user_kbs.main_kb)
        return
    
    await callback.message.answer('Вы не пополнили баланс',
                                    reply_markup=user_kbs.check_dep_kb)


@router.callback_query(F.data == 'promo')
async def promo(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('Промокоды: ...')


@router.callback_query(F.data == 'learning')
async def promo(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('Обучение')


@router.callback_query(F.data == 'news')
async def promo(callback: CallbackQuery):
    await callback.answer()
    news = await get_current_news()

    message_text = ''
    for n in news:
        message_text += f'Время: {n["time"]}\nВалюта:{n["currency"]}\nСобытие {n["title"]}\n\n'
    
    await callback.message.answer(message_text)


@router.callback_query(F.data == 'statistics')
async def statistics(callback: CallbackQuery, stat_service: StatService):
    await callback.answer()
    
    now = datetime.now(timezone(timedelta(hours=3)))
    yesterday = now - timedelta(days=1)
    yesterday_date = yesterday.strftime('%d.%m.%Y')
    
    
    yesterday_stat = await stat_service.get_last_day()
    
    if not yesterday_stat or yesterday_stat.date != yesterday_date:
        await stat_service.add(
            yesterday_date,
            randint(710, 1010),
            randint(110, 310),
            randint(5, 30)
        )
    
    last_week = await stat_service.get_last_week()
    
    message_text = ''
    for day in last_week:
        message_text += f'Дата: {day.date}\nПрофиты: {day.profit}\nМинусы: {day.loss}\nВозврат: {day.break_even}\nВинрейт: {round(day.profit / (day.loss + day.profit) * 100)}%\n\n'
    
    await callback.message.answer(message_text)


@router.callback_query(F.data == 'change_otc')
async def change_otc(callback: CallbackQuery, user_service: UserService):
    await callback.answer()
    otc = await user_service.change_otc(callback.from_user.id)
    
    try:
        await callback.message.edit_reply_markup(
            inline_message_id=callback.inline_message_id,
            reply_markup=user_kbs.forecast_menu(otc)
        )
    except:
        pass

@router.callback_query(F.data == 'menu')
async def menu(callback: CallbackQuery):
    await callback.answer()
    image = FSInputFile('images/photo.jpg')
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer_photo(image, caption='у вас есть доступ к функциям',
                                        reply_markup=user_kbs.main_kb)


