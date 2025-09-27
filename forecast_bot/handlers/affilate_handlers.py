from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ContentType, InputMediaVideo, FSInputFile
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from forecast_bot.states.user_states import AffiliateState
from forecast_bot.keyboards import user_kbs
from forecast_bot.init_bot import bot
from config import admin_username

import os


load_dotenv()

router = Router()


@router.message(Command('free'))
async def affilate_handler(message: Message):
    await message.answer_photo(FSInputFile('images/affilate.jpg'), caption=f'<b>Если ты хочешь начать торговать, но у тебя нет средств на депозит, то мы можем тебе помочь.\n\nУ нас есть партнерская программа, где все очень просто – ты выкладываешь видео, мы платим тебе за просмотры.\n\nАктуальные расценки:\n5.000 просмотров – 100$\n20.000 просмотров – 500$\n100.000 просмотров – 3 000$\n\nПросмотры учитываются с TikTok и YouTube (можем обговорить ваши источники трафика, если таковые имеются).\n\nПо вопросам – @{admin_username}\n\nУдачи!</b>',
                            reply_markup=user_kbs.affilate_bio_kb)


@router.callback_query(F.data == 'affilate_earning')
async def affilate_earning_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await callback.message.edit_caption(caption='<b>Отлично! Напиши нам, как ты планируешь зазывать аудиторию в бота. \nЧем больше информации, тем лучше\n\n<blockquote>Пример: «Я Иван, занимаюсь продвижением проектов, снимаю в ТикTok – https://ссылка-на-тикток, и планирую начать снимать на YouTube»</blockquote>\n\nЕсли ты ранее не занимался продвижением проектов, ничего страшного, просто опиши, \nгде и какие будешь выкладывать видео 😉</b>',
                                    reply_markup=user_kbs.affilate_back_kb)
    
    await state.set_state(AffiliateState.user_info)


@router.callback_query(F.data == 'affilate_back')
async def affilate_back_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_caption(caption=f'<b>Если ты хочешь начать торговать, но у тебя нет средств на депозит, то мы можем тебе помочь.\n\nУ нас есть партнерская программа, где все очень просто – ты выкладываешь видео, мы платим тебе за просмотры.\n\nАктуальные расценки:\n5.000 просмотров – 100$\n20.000 просмотров – 500$\n100.000 просмотров – 3 000$\n\nПросмотры учитываются с TikTok и YouTube (можем обговорить ваши источники трафика, если таковые имеются).\n\nПо вопросам – @{admin_username}\n\nУдачи!</b>',
                            reply_markup=user_kbs.affilate_bio_kb)
    await state.clear()

@router.message(AffiliateState.user_info)
async def user_info_handler(message: Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer('<b>Можно отправлять только текст. Если хотите приложить к тексту что-то еще, пишите - </b>')
        return

    await bot.send_message(os.getenv('ADMIN_ID'), f'Заявка на партенрство от {message.from_user.id}\nUsername: @{message.from_user.username}\n\n{message.text}', parse_mode=None)
    
    await message.answer(f'<b>Благодарим за заявку. Теперь можете выкладывать видео с нашим роботом и зарабатывать на просмотрах\nПоддержка/выплаты - @{admin_username}</b>',
                            reply_markup=user_kbs.affilate_videos_kb)
    await state.clear()


@router.callback_query(F.data == 'affilate_videos')
async def affilate_videos_handler(callback: CallbackQuery):
    await callback.answer()
    
    download_message = await callback.message.answer('<b>Загрузка...</b>')
    try:
        await callback.message.delete()
    except:
        pass
    
    media = [
        InputMediaVideo(media=FSInputFile('videos/video_1.mp4'), caption=f'<b>Примеры работ, если у вас есть идеи, можете обговорить их с @{admin_username}</b>'),
        InputMediaVideo(media=FSInputFile('videos/video_2.mp4')),
        InputMediaVideo(media=FSInputFile('videos/video_3.mp4')),
    ]
    
    await callback.message.answer_media_group(media)
    await download_message.delete()