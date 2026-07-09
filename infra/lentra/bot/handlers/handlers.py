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



def human_decision(action: str) -> str:

    return {
        "ACCEPT": "🟢 Можно рассматривать",
        "REVIEW": "🟡 Требует проверки",
        "REJECT": "🔴 Лучше избегать"
    }.get(
        action,
        "⚪ Требуется анализ"
    )



def build_explanation(
    decision: dict,
    market: dict,
    risk_level: str
) -> str:

    action = decision.get(
        "action",
        "REVIEW"
    )

    difference = market.get(
        "difference_percent",
        0
    )


    if risk_level == "high":

        return (
            "Цена выглядит привлекательной, "
            "но высокий риск объявления. "
            "Не рекомендуется без проверки владельца "
            "и просмотра объекта."
        )


    if action == "ACCEPT":

        return (
            f"Цена значительно ниже рынка "
            f"({difference}%). "
            "Хорошее предложение, рекомендуется "
            "проверить состояние объекта."
        )


    if action == "REVIEW":

        if difference > 5:

            return (
                "Цена выше рынка. "
                "Стоит сравнить альтернативные варианты."
            )


        return (
            "Цена соответствует рынку. "
            "Рекомендуется проверить детали объекта."
        )


    return (
        "Объект имеет негативные сигналы рынка."
    )



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


        market = intelligence.get(
            "market",
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


        action = decision.get(
            "action",
            "REVIEW"
        )


        score = decision.get(
            "score",
            0
        )


        ranking_score = ranking.get(
            "ranking_score",
            0
        )


        ranking_percent = round(
            ranking_score * 100,
            1
        )


        difference = market.get(
            "difference_percent",
            0
        )


        explanation = build_explanation(
            decision,
            market,
            risk_level
        )


        lines.append(
            f"""
🏠 {title}

💵 Цена:
${price}/месяц

📈 Рынок:
${market_price}

{human_decision(action)}

🤖 AI решение:
{action}

⭐ Score:
{round(score, 3)}

📉 Отклонение от рынка:
{difference}%

⚠️ Риск:
{risk_level}

🔁 Дубли:
{duplicates}

🏆 Рыночный рейтинг:
{ranking_percent}/100

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
