from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ContentType, CallbackQuery
from aiogram.fsm.context import FSMContext

from forecast_bot.middlewares.db_di import DatabaseDI
from database.services.user_service import UserService
from database.services.trader_data_service import TraderDataService
from forecast_bot.states.user_states import UserDataState
from forecast_bot.keyboards import user_kbs


router = Router()
router.message.middleware(DatabaseDI())


@router.message(CommandStart())
async def start_handler(message: Message, user_service: UserService, trader_data_service: TraderDataService):
    tg_id = message.from_user.id
    
    await user_service.create_if_not_exists(tg_id)
    trader_data = await trader_data_service.get_by_tg_id(tg_id)
    
    if not trader_data:
        await message.answer('Вы еще не зарегестрированы, нажмите кнопку далее чтобы получить доступ',
                                reply_markup=user_kbs.start_left_kb)
        return

    if trader_data.balance > 0:
        await message.answer('Вы уже зарегестрированы и у вас есть доступ к функциям')
        return
    
    await message.answer('Вы зарегестрированы, пополните баланс на любую сумму и нажмите кнопку ниже чтобы проверить депозит',
                            reply_markup=user_kbs.check_dep_kb)


@router.callback_query(F.data == 'get_access')
async def get_access(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('скинь id')
    await state.set_state(UserDataState.trader_id)


@router.message(UserDataState.trader_id)
async def check_trader_id(message: Message, trader_data_service: TraderDataService, state: FSMContext):
    trader_id = int(message.text) if message.text.isdigit() else -1
    res = await trader_data_service.check_trader_id(trader_id, message.from_user.id)
    
    if res:
        await message.answer('привязанр')
        await state.clear()
        return
    
    await message.answer('не тот id')


@router.callback_query(F.data == 'check_dep')
async def check_dep(callback: CallbackQuery, trader_data_service: TraderDataService):
    await callback.answer()
    
    trader_data = await trader_data_service.get_by_tg_id(callback.from_user.id)
    
    if trader_data.balance > 0:
        await callback.message.answer('Вы успешно получилс доступ')
        return
    
    await callback.message.answer('Вы не пополнили баланс',
                                    reply_markup=user_kbs.check_dep_kb)