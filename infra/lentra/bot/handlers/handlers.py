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


    result = data.get(
        "result",
        {}
    )


    results = result.get(
        "results",
        []
    )


    if not results:
        return "Ничего не найдено"


    snapshot = result.get(
        "market_snapshot",
        {}
    )


    lines = []


    lines.append(
        f"🏠 Найдено объектов: {len(results)}"
    )


    lines.append(
        f"📊 Цена рынка: ${snapshot.get('median_price')}"
    )


    lines.append("")


    for item in results[:5]:

        title = item.get(
            "title",
            "Object"
        )


        price = item.get(
            "price",
            0
        )


        ranking = item.get(
            "ranking",
            {}
        )


        market_price = ranking.get(
            "market_price",
            snapshot.get(
                "median_price",
                0
            )
        )


        decision = item.get(
            "decision",
            {}
        )


        intelligence = item.get(
            "intelligence",
            {}
        )


        risk = intelligence.get(
            "risk",
            {}
        ).get(
            "risk",
            {}
        )


        dedup = intelligence.get(
            "dedup",
            {}
        )


        risk_level = risk.get(
            "level",
            "unknown"
        )


        duplicates = dedup.get(
            "duplicates",
            0
        )


        ranking_score = ranking.get(
            "ranking_score",
            0
        )


        action = decision.get(
            "action",
            "REVIEW"
        )


        score = decision.get(
            "score",
            0
        )


        lines.append(
            f"""
🏠 {title}

💵 Цена: ${price}
📈 Рынок: ${market_price}

🎯 Решение: {action}
⭐ Score: {score}

⚠️ Риск: {risk_level}
🔁 Дубли: {duplicates}

🏆 Ranking: {ranking_score}
"""
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
