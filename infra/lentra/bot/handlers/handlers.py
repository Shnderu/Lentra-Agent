from aiogram import Router, F
from aiogram.types import Message

import httpx
import logging


router = Router()

logger = logging.getLogger(__name__)


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

    if data.get("status") != "ok":
        return "❌ Ошибка анализа рынка"

    result = data.get("result", {})

    snapshot = result.get(
        "market_snapshot",
        {}
    )

    listings = snapshot.get(
        "clean_listings",
        []
    )

    if not listings:
        return "Ничего не найдено"


    lines = []

    lines.append(
        f"🏠 Найдено объектов: {len(listings)}"
    )

    lines.append(
        f"📊 Средняя цена рынка: ${snapshot.get('median_price')}"
    )

    lines.append("")


    for item in listings[:5]:

        price = item.get(
            "price"
        )

        market = item.get(
            "market_price"
        )

        risk = item.get(
            "risk"
        )

        title = item.get(
            "title",
            "Object"
        )


        lines.append(
            f"🏠 {title}\n"
            f"💵 Цена: ${price}\n"
            f"📈 Рынок: ${market}\n"
            f"⚠️ Риск: {risk}\n"
        )


    return "\n".join(lines)



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
