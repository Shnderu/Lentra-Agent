from telethon import TelegramClient
from lentra.connectors.telegram_connector.parser import TelegramPropertyParser
from lentra.property.models import Property
import os


class TelegramLiveConnector:

    def __init__(self):
        self.api_id = int(os.getenv("TG_API_ID", "0"))
        self.api_hash = os.getenv("TG_API_HASH", "")
        self.channel = os.getenv("TG_CHANNEL", "DomikoVietnam")

        self.client = TelegramClient(
            "lentra_session",
            self.api_id,
            self.api_hash
        )

    async def search(self, query: str = None):

        await self.client.start()

        messages = await self.client.get_messages(
            self.channel,
            limit=20
        )

        results = []

        for msg in messages:

            if not msg.message:
                continue

            parsed = TelegramPropertyParser.parse(msg.message)

            results.append(
                Property(
                    id=str(msg.id),
                    source="telegram_live",
                    title=msg.message.split("\n")[0],
                    url=None,
                    city="Vietnam",
                    price=parsed.get("price") or 0,
                    deposit=parsed.get("deposit"),
                    bedrooms=parsed.get("bedrooms"),
                    bathrooms=parsed.get("bathrooms"),
                    area_m2=parsed.get("area_m2"),
                    pet_friendly=parsed.get("pet_friendly"),
                    pool=parsed.get("pool"),
                    sea_view=parsed.get("sea_view"),
                    trust_score=75,
                    photos=[],
                    metadata={"tg_id": msg.id}
                )
            )

        await self.client.disconnect()

        return results
