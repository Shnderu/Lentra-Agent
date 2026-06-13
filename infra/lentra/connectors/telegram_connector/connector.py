from lentra.property.models import Property
from lentra.connectors.telegram_connector.parser import TelegramPropertyParser


class TelegramConnector:

    def __init__(self, raw_messages: list[str]):
        self.raw_messages = raw_messages

    async def search(self, query: str = None):

        results = []

        for msg in self.raw_messages:

            parsed = TelegramPropertyParser.parse(msg)

            results.append(
                Property(
                    id=str(hash(msg)),
                    source="telegram_domiko",
                    title=msg.split("\n")[0],
                    url="",
                    city="Vietnam",
                    price=parsed.get("price") or 0,
                    deposit=parsed.get("deposit"),
                    bedrooms=parsed.get("bedrooms"),
                    bathrooms=parsed.get("bathrooms"),
                    area_m2=parsed.get("area_m2"),
                    pet_friendly=parsed.get("pet_friendly"),
                    pool=parsed.get("pool"),
                    sea_view=parsed.get("sea_view"),
                    trust_score=70,
                    photos=[],
                    metadata={"raw": msg}
                )
            )

        return results
