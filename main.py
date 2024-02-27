import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from config import BOT_TOKEN
from handlers.category_handlers import category_router
from handlers.cmd_handlers import cmd_router
from handlers.product_handlers import product_router


async def main():
    bot = Bot(
        token=BOT_TOKEN,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )
    dp = Dispatcher()
    dp.include_routers(cmd_router, category_router, product_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
