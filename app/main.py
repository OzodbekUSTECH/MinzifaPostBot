import asyncio
import logging
import sys

from aiogram import Dispatcher

from app.presentation.aiogram_bot.v1.routers import include_all_routers

from app.infrastructure.config import bot, settings
from app.presentation.aiogram_bot.v1.middlewares.access import AccessMiddleware


async def main() -> None:

    dp = Dispatcher()
    include_all_routers(dp=dp)

    dp.message.middleware(AccessMiddleware(allowed_usernames=settings.USERNAMES))

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
