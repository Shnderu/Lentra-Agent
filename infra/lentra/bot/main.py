import asyncio
import logging

from aiogram import Bot, Dispatcher

from lentra.bot.config import BOT_TOKEN
from lentra.bot.handlers.handlers import router as search_router


logging.basicConfig(
    level=logging.INFO
)


async def main():

    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is empty"
        )

    bot = Bot(
        token=BOT_TOKEN
    )

    dp = Dispatcher()


    #
    # Primary user interaction router
    #
    dp.include_router(
        search_router
    )


    logging.info(
        "[BOT] starting aiogram polling"
    )


    try:

        await dp.start_polling(
            bot
        )

    finally:

        await bot.session.close()



if __name__ == "__main__":

    asyncio.run(
        main()
    )
