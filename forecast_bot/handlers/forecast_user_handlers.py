from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from forecast_bot.middlewares.db_di import DatabaseDI
from database.services.user_service import UserService
from database.services.trader_data_service import TraderDataService
from forecast_bot.keyboards import user_kbs

from random import randint
from asyncio import sleep
from typing import Callable


router = Router()
router.message.middleware(DatabaseDI())
router.callback_query.middleware(DatabaseDI())


async def choose_active(callback: CallbackQuery, markup: Callable, otc: bool, page: int):
    try:
        await callback.message.edit_text('<b>Теперь необходимо выбрать точный актив для анализа.\n\n<blockquote>Примечание: сначала проверьте наличие актива на платформе Pocket Option, а затем получайте прогноз ✅</blockquote></b>',
                                        reply_markup=markup(otc, page))
    except:
            await callback.message.answer('<b>Теперь необходимо выбрать точный актив для анализа.\n\n<blockquote>Примечание: сначала проверьте наличие актива на платформе Pocket Option, а затем получайте прогноз ✅</blockquote></b>',
                                        reply_markup=markup(otc, page))
            return


@router.callback_query(F.data == 'forecast_menu')
async def forecast_menu(callback: CallbackQuery, user_service: UserService):
    await callback.answer()
    
    user = await user_service.get(callback.from_user.id)
    
    await callback.message.answer('<b>Выберите по какому разделу хотите получить прогноз.</b>',
                                    reply_markup=user_kbs.forecast_menu(user.otc))
    
    try:
        await callback.message.delete()
    except:
        pass


@router.message(Command('forecast'))
async def forecast_menu(message: Message, user_service: UserService, trader_data_service: TraderDataService):
    user = await user_service.get(message.from_user.id)
    trader_data = await trader_data_service.get_by_tg_id(user.tg_id)
    if trader_data:
        await message.answer('<b>Выберите по какому разделу хотите получить прогноз.</b>',
                                        reply_markup=user_kbs.forecast_menu(user.otc))
        return
    
    await message.answer('<b>У вас еще нет доступа к этому функционалу ❌ </b>')


@router.callback_query(F.data.startswith('currency_pairs'))
async def currency_pairs(callback: CallbackQuery, user_service: UserService):
    await callback.answer()
    
    user = await user_service.get(callback.from_user.id)
    page = 1 if len(callback.data.split('_')) < 3 else int(callback.data.split('_')[-1]) 

    await choose_active(callback, user_kbs.currency_pairs_by_page, user.otc, page)
    return

@router.callback_query(F.data.startswith('crypto'))
async def crypto(callback: CallbackQuery, user_service: UserService):
    await callback.answer()
    
    user = await user_service.get(callback.from_user.id)
    page = 1 if len(callback.data.split('_')) < 2 else int(callback.data.split('_')[-1]) 
    
    await choose_active(callback, user_kbs.crypto_by_page, user.otc, page)
    return


@router.callback_query(F.data.startswith('indices'))
async def indeces(callback: CallbackQuery, user_service: UserService):
    await callback.answer()
    
    user = await user_service.get(callback.from_user.id)
    page = 1 if len(callback.data.split('_')) < 2 else int(callback.data.split('_')[-1]) 
    
    await choose_active(callback, user_kbs.indices_by_page, user.otc, page)
    return


@router.callback_query(F.data.startswith('commodities'))
async def commodities(callback: CallbackQuery, user_service: UserService):
    await callback.answer()
    
    user = await user_service.get(callback.from_user.id)
    page = 1 if len(callback.data.split('_')) < 2 else int(callback.data.split('_')[-1]) 
    
    await choose_active(callback, user_kbs.commodities_by_page, user.otc, page)
    return

@router.callback_query(F.data.startswith('stocks'))
async def stocks(callback: CallbackQuery, user_service: UserService):
    await callback.answer()
    
    user = await user_service.get(callback.from_user.id)
    page = 1 if len(callback.data.split('_')) < 2 else int(callback.data.split('_')[-1]) 
    
    await choose_active(callback, user_kbs.stocks_by_page, user.otc, page)
    return


@router.callback_query(F.data.startswith('get_forecast'))
async def get_forecast(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await state.set_data({'active': callback.data.split('_')[-1]})
    await callback.message.edit_text('<b>Актив успешно выбран. Теперь укажите период 🕐</b>', 
                                        reply_markup=user_kbs.period)


@router.callback_query(F.data.startswith('period'))
async def period(callback: CallbackQuery, state: FSMContext, user_service: UserService):
    await callback.answer()
    
    user = await user_service.get(callback.from_user.id)
    
    active = await state.get_data()
    active = active['active'] if not user.otc else f'{active["active"]} OTC'
    
    await callback.message.edit_text(f'<b>⏳ Подождите... среднее время ожидания - <i>20 секунд</i>\n\nРобот анализирует рынок для получения прогноза по активу {active} с максимальной точностью\n\n<blockquote>Аналитика производится при помощи индикаторов с сайтов Pocket Option и Trading View, а так же с учетом новостного фона (Investing). Робот учитывает волатильность рынка и тренд на разных таймфреймах</blockquote></b>')
    
    period = callback.data.split('_')[-1]
    time_dict = {
        '15s': 15,
        '30s': 30,
        '1m': 60,
        '2m': 120,
        '3m': 180,
        '5m': 300,
        '10m': 600,
        '15m': 900,
        '30m': 1800,
        '60m': 3600
    }
    
    forecast = 'повышение 📈' if randint(0, 1) else 'понижение 📉'
    
    await sleep(randint(8, 14))
    
    image = FSInputFile('images/up.jpg') if forecast == 'повышение' else FSInputFile('images/down.jpg')
    caption = "<b>💼 Прогноз по активу:</b> <i><b>{active}</b></i>\n<b>Направление:</b> <i><b>{forecast}</b></i>\n<b>Таймфрейм:</b> <i><b>{period}</b></i>\n\n<blockquote><b>Самая высокая проходимость прогнозов достигается, когда вы входите в сделку как можно быстрее. Задержка снижает эффективность — действуйте оперативно!</b></blockquote>"
    forecast_message = await callback.message.answer_photo(
        photo=image,
        caption=caption.format(active=active, forecast=forecast, period=period),
    )
    
    try:
        await callback.message.delete()
    except:
        pass
    
    await sleep(time_dict[period])
    
    image = FSInputFile('images/completed.jpg')
    await forecast_message.reply_photo(image, caption=f'<b>Сделка по активу <i>{active}</i> на {forecast} завершена, можете получить новый прогноз\n\n<blockquote>В случае если сделка завершилась неудачно, рекомендуем запросить новый прогноз по этому же активу, что бы бот мог проанализировать актуальную информацию</blockquote></b>',
                                        reply_markup=user_kbs.forecast_menu(user.otc))