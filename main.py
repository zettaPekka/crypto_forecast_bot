import asyncio
from aiogram import Dispatcher
import uvicorn

from forecast_bot.init_bot import bot
from forecast_bot.handlers.user_handlers import router as user_router
from forecast_bot.handlers.forecast_user_handlers import router as forecast_user_router
from database.database import init_db
from app.init_app import app

import logging


async def run_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    
    dp = Dispatcher()
    dp.include_routers(user_router, forecast_user_router)
    
    await dp.start_polling(bot)

async def run_app():
    config = uvicorn.Config('main:app')
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    logging.basicConfig(level=logging.INFO)
    
    await init_db()
    
    await asyncio.gather(
        run_bot(),
        run_app(),
    )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass