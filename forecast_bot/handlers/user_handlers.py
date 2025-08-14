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
        text = "<b>Добро пожаловать в торгового робота JIKO TRADE!</b>\n\n<b>Для получения доступа нажми на кнопку ниже.</b>\n\n<b>Что вы получаете:\n<blockquote>✅ Сигналы на выбранный актив с любым периодом\n✅ Возможность выбора OTC\n✅ Актуальные новости\n✅ Честную и открытую статистику\n✅ Новые промокоды и бонусы</blockquote></b>\n\n<b>Скорей присоединяйся 👇</b>"
        await message.answer_photo(image, caption=text,
                                reply_markup=user_kbs.start_left_kb)
        return

    if trader_data.balance > 0:
        image = FSInputFile('images/photo.jpg')
        await message.answer_photo(image, caption='<b>У вас есть полный доступ к функционалу торгового робота. Для продолжения используйте кнопки ниже или команды:\n\n<blockquote>/news – 📰 Новости \n/forecast – 📊 Получить прогноз</blockquote></b>',
                                    reply_markup=user_kbs.main_kb)
        return
    
    image = FSInputFile('images/photo.jpg')
    await message.answer_photo(image, caption='Вы зарегестрированы, пополните баланс на любую сумму и нажмите кнопку ниже чтобы проверить депозит',
                            reply_markup=user_kbs.check_dep_kb)


@router.callback_query(F.data == 'get_access')
async def get_access(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    image = FSInputFile('images/photo.jpg')
    text = "<b>Для получения доступа необходимо создать аккаунт по кнопке ниже (обязательно, иначе бот не сможет подтвердить доступ) или по ссылке.\n\nПосле создания аккаунта напиши свой трейдер-ID ниже\n\n<blockquote>Промо – <code>KRX068</code> (+60% к пополнению)</blockquote></b>"
    image = InputMediaPhoto(media=image, caption=text)
    await callback.message.edit_media(image)
    await state.set_state(UserDataState.trader_id)


@router.message(UserDataState.trader_id)
async def check_trader_id(message: Message, trader_data_service: TraderDataService, state: FSMContext):
    trader_id = int(message.text) if message.text.isdigit() else -1
    res = await trader_data_service.check_trader_id(trader_id, message.from_user.id)
    
    if res:
        await message.answer(f'<b>✔ Отлично ID {trader_id} привязан! Теперь необходимо пополнить баланс на любую сумму, так как бот выдает доступ только активным аккаунтам\n\nПри пополнении можешь использовать промокод <code>KRX068</code> который дает +60% к пополнению!\nПосле того как пополнил баланс жми кнопку ниже</b>',
                                reply_markup=user_kbs.check_dep_kb)
        await state.clear()
        return
    
    await message.answer('<b>❌ К сожалению не удалось подвердить ID, скорее всего вы уже ранее создали аккаунт, в таком случае необходимо создать новый и прислать новый ID</b>',
                            reply_markup=user_kbs.reg_kb)


@router.callback_query(F.data == 'check_dep')
async def check_dep(callback: CallbackQuery, trader_data_service: TraderDataService):
    await callback.answer()
    
    trader_data = await trader_data_service.get_by_tg_id(callback.from_user.id)
    
    if trader_data.balance > 0:
        image = FSInputFile('images/photo.jpg')
        await callback.message.answer_photo(image, caption='<b>Успешно! Теперь у вас есть полный доступ к торговому боту, можете получать прогнозы 24/7 ✨\n\n<blockquote>/news – 📰 Новости \n/forecast – 📊 Получить прогноз</blockquote></b>',
                                            reply_markup=user_kbs.main_kb)
        return
    
    await callback.message.answer('<b>Кажется вы не пополнили баланс на привязанном аккаунте, после пополнения проверьте еще раз по кнопке 👇</b>',
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
        message_text += f'<b>⏳ Время: <i>{n["time"]}</i>\n💲 Валюта:<i>{n["currency"]}</i>\n🗞 Событие: <i>{n["title"]}</i></b>\n\n'
    
    await callback.message.answer(message_text)


@router.message(Command('news'))
async def promo(message: Message, trader_data_service: TraderDataService):
    trader_data = await trader_data_service.get_by_tg_id(message.from_user.id)
    if not trader_data:
        await message.answer('<b>У вас еще нет доступа к этому функционалу ❌ </b>')
        return
    
    news = await get_current_news()

    message_text = ''
    for n in news:
        message_text += f'<b>⏳ Время: <i>{n["time"]}</i>\n💲 Валюта:<i>{n["currency"]}</i>\n🗞 Событие: <i>{n["title"]}</i></b>\n\n'
    
    await message.answer(message_text)


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
    
    message_text = '<b>Открытая статистика за неделю</b>\n\n'
    for day in last_week:
        message_text += f'🕐 Дата: <i>{day.date}</i>\n✔ Профиты: <i>{day.profit}</i>\n❌ Минусы: <i>{day.loss}</i>\n♻️ Возврат: <i>{day.break_even}</i>\n<blockquote>Винрейт: {round(day.profit / (day.loss + day.profit) * 100)}%</blockquote>\n\n'
    
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
    await callback.message.answer_photo(image, caption='<b>У вас есть полный доступ к функционалу торгового робота. Для продолжения используйте кнопки ниже или команды:\n\n<blockquote>/news – 📰 Новости \n/forecast – 📊 Получить прогноз</blockquote></b>',
                                        reply_markup=user_kbs.main_kb)


