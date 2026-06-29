import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message

from lentra.telegram.config import BOT_TOKEN
from lentra.telegram.bot import LentraBot
from lentra.core.market_intelligence.market_intelligence_engine import MarketIntelligenceEngine

engine = MarketIntelligenceEngine()
core_bot = LentraBot(engine)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_message(message: Message):

    update = {"text": message.text}

    result = core_bot.handle(update)

    if isinstance(result, list):
        for r in result:
            await message.answer(r)
    else:
        await message.answer(str(result))


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
