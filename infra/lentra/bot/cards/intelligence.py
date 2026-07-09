from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class IntelligenceCard:

    id: str
    title: str
    text: str
    raw: Dict[str, Any]


class IntelligenceCardBuilder:


    def build(self, item: dict) -> IntelligenceCard:

        card = item.get(
            "card",
            {}
        )

        price = card.get(
            "price",
            0
        )

        market = card.get(
            "market_price",
            0
        )

        risk = card.get(
            "risk",
            {}
        )

        duplicates = card.get(
            "duplicates",
            0
        )

        explanation = card.get(
            "explanation",
            ""
        )

        decision = card.get(
            "decision",
            {}
        )

        score = decision.get(
            "score",
            0
        )


        text = f"""
🏠 {item.get('title','Object')}

💰 Цена:
${price}/месяц

📈 Рынок:
${market}

🤖 AI оценка:
{round(score * 100)}/100

⚠️ Риск:
{risk.get('level','unknown')}

🔁 Похожие объявления:
{duplicates}

💡 Анализ:

{explanation}
"""


        return IntelligenceCard(
            id=str(
                item.get(
                    "id",
                    ""
                )
            ),
            title=item.get(
                "title",
                ""
            ),
            text=text.strip(),
            raw=item
        )
