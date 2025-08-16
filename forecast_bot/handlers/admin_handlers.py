from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

from database.services.user_service import UserService
from database.services.trader_data_service import TraderDataService
from forecast_bot.middlewares.db_di import DatabaseDI

import os


load_dotenv()

router = Router()
router.message.middleware(DatabaseDI())


@router.message(Command('admin'))
async def admin_handler(message: Message, user_service: UserService, trader_data_service: TraderDataService):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        users_count = len(await user_service.get_all_users())
        reg_users = len(await trader_data_service.get_reg_traders())
        active_users = len(await trader_data_service.get_active_traders())
        
        await message.answer(f'<b>Количество пользователей: {users_count}\nПодтвердивших ID: {reg_users}\nАктивных: {active_users}</b>')