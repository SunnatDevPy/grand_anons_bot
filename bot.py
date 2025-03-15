import asyncio
import logging
import sys

from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand

from bot.handlers.bot_announse import bot_anons_router
from bot.handlers.shop import shop_router
from bot.handlers.shop_biznes import shop_business_router
from bot.handlers.shop_home import shop_home

from bot.handlers.start import start_router

from dispatcher import bot
from models import db


async def on_start(bot: Bot):
    commands_admin = [
        BotCommand(command='start', description="Рестарт бота")
    ]
    await bot.set_my_commands(commands=commands_admin)
    await db.create_all()


async def on_shutdown(bot: Bot):
    await bot.delete_my_commands()


async def main():
    dp = Dispatcher()
    dp.include_routers(start_router, bot_anons_router, shop_business_router, shop_router, shop_home)
    dp.startup.register(on_start)
    dp.shutdown.register(on_shutdown)
    # dp.update.middleware(handle_chat_join_request)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

# 1065  docker login
# 1068  docker build -t nickname/name .
# 1071  docker push nickname/name

# docker run --name db_mysql -e MYSQL_ROOT_PASSWORD=1 -d mysql
