from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from database.services.user_service import UserService
from database.services.trader_data_service import TraderDataService
from forecast_bot.middlewares.db_di import DatabaseDI
import forecast_bot.keyboards.admin_kbs as adm_kbs
from forecast_bot.states.admin_states import AdminState
from forecast_bot.init_bot import bot

import os


load_dotenv()

router = Router()
router.message.middleware(DatabaseDI())
router.callback_query.middleware(DatabaseDI())


@router.message(Command('admin'))
async def admin_handler(message: Message, user_service: UserService, trader_data_service: TraderDataService):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        users_count = len(await user_service.get_all_users())
        reg_users = len(await trader_data_service.get_reg_traders())
        active_users = len(await trader_data_service.get_active_traders())
        
        await message.answer(f'<b>Количество пользователей: {users_count}\nПодтвердивших ID: {reg_users}\nАктивных: {active_users}</b>',
                                reply_markup=adm_kbs.send_kb)


@router.callback_query(F.data == 'sending')
async def sending_content(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await callback.message.edit_text('Введите контент для рассылки',
                                    reply_markup=adm_kbs.back_kb)
    await state.set_state(AdminState.content)


@router.callback_query(F.data == 'cancel')
async def sending_content(callback: CallbackQuery, state: FSMContext, user_service: UserService, trader_data_service: TraderDataService):
    await callback.answer()
    
    users_count = len(await user_service.get_all_users())
    reg_users = len(await trader_data_service.get_reg_traders())
    active_users = len(await trader_data_service.get_active_traders())
    
    await callback.message.edit_text(f'<b>Количество пользователей: {users_count}\nПодтвердивших ID: {reg_users}\nАктивных: {active_users}</b>',
                                reply_markup=adm_kbs.send_kb)
    await state.clear()

@router.message(AdminState.content)
async def send_mails(message: Message, state: FSMContext, user_service: UserService):
    users = await user_service.get_all_users()
    users_id = [user.tg_id for user in users]
    
    succes_users = 0
    if message.content_type == ContentType.TEXT:
        await state.clear()
        for user_id in users_id:
            try:
                await bot.send_message(user_id, message.text)
                succes_users += 1
            except:
                pass
    elif message.content_type == ContentType.PHOTO:
        await state.clear()
        for user_id in users_id:
            try:
                await bot.send_photo(user_id, photo=message.photo[-1].file_id, caption=message.caption)
                succes_users += 1
            except:
                pass
    elif message.content_type == ContentType.VIDEO:
        await state.clear()
        for user_id in users_id:
            try:
                await bot.send_video(user_id, video=message.video.file_id, caption=message.caption)
                succes_users += 1
            except:
                pass
    elif message.content_type == ContentType.STICKER:
        await state.clear()
        for user_id in users_id:
            try:
                await bot.send_sticker(user_id, sticker=message.sticker.file_id)
                succes_users += 1
            except:
                pass
    elif message.content_type == ContentType.ANIMATION:
        await state.clear()
        for user_id in users_id:
            try:
                await bot.send_animation(user_id, animation=message.animation.file_id, caption=message.caption)
                succes_users += 1
            except:
                pass
    elif message.content_type == ContentType.VIDEO_NOTE:
        await state.clear()
        for user_id in users_id:
            try:
                await bot.send_video_note(user_id, video_note=message.video_note.file_id)
                succes_users += 1
            except:
                pass
    else:
        await message.answer('Неправильный формат, попробуй еще раз',
                                    reply_markup=adm_kbs.back_kb)
        return
    await message.answer(f'Раcсылка окончена, отправлено {succes_users} пользователям')
