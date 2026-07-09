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


    median_price = snapshot.get(
        "median_price",
        0
    )


    lines = []


    lines.append(
        f"🏠 Найдено объектов: {len(results)}"
    )

    lines.append(
        f"📊 Рынок Da Nang: ${median_price}/месяц"
    )

    lines.append(
        ""
    )


    for item in results[:5]:

        title = item.get(
            "title",
            "Object"
        )


        card = item.get(
            "card",
            {}
        )


        price = card.get(
            "price",
            0
        )


        market_price = card.get(
            "market_price",
            median_price
        )


        difference = card.get(
            "difference_percent",
            0
        )


        risk = card.get(
            "risk",
            {}
        )


        risk_level = risk.get(
            "level",
            "unknown"
        )


        duplicates = card.get(
            "duplicates",
            0
        )


        decision = card.get(
            "decision",
            {}
        )


        action = decision.get(
            "action",
            "REVIEW"
        )


        score = decision.get(
            "score",
            0
        )


        explanation = card.get(
            "explanation",
            ""
        )


        if action == "ACCEPT":

            verdict = "🟢 Хорошее предложение"

        elif action == "REJECT":

            verdict = "🔴 Лучше избегать"

        else:

            verdict = "🟡 Требует проверки"


        lines.append(
            f"""
━━━━━━━━━━━━

🏠 {title}

💰 Цена:
${price}/месяц

📈 Рынок:
${market_price}

{verdict}

🤖 AI оценка:
{round(score * 100)}/100


📉 Отклонение:
{difference}%


⚠️ Риск:
{risk_level}


🔁 Похожие объявления:
{duplicates}


💡 Анализ:
{explanation}
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
