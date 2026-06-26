import asyncio
from lentra.telegram.bot import Bot
from lentra.telegram.bot_factory import create_bot as create_real_bot


def create_bot():
    bot = create_real_bot()
    return bot


if __name__ == "__main__":
    bot = create_bot()

    if hasattr(bot, "run") and asyncio.iscoroutinefunction(bot.run):
        asyncio.run(bot.run())
    else:
        bot.run()
