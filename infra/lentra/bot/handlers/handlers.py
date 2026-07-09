from aiogram import Router, F
from aiogram.types import Message

import httpx
import logging

from lentra.bot.cards.intelligence_renderer import IntelligenceCardRenderer


router = Router()

logger = logging.getLogger(__name__)

intelligence_renderer = IntelligenceCardRenderer()


SEARCH_API_URL = "http://localhost:8000/search"


def build_message_router(container):
    return router


async def call_search_api(query: str):

    payload = {
        "query": query
    }

    async with httpx.AsyncClient(timeout=20) as client:

        response = await client.post(
            SEARCH_API_URL,
            json=payload
        )

        response.raise_for_status()

        return response.json()



def format_result(data: dict) -> str:

    return intelligence_renderer.render(data)



@router.message(F.text)
async def handle_search(message: Message):

    query = message.text.strip()


    try:

        data = await call_search_api(
            query
        )


        text = format_result(
            data
        )


        await message.answer(
            text
        )


    except Exception as e:

        logger.exception(
            "[BOT SEARCH ERROR]"
        )


        await message.answer(
            f"Ошибка поиска: {e}"
        )
