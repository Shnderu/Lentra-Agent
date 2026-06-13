import os
import asyncio
from telethon import TelegramClient, events

from lentra.pipeline.property_pipeline import PropertyPipeline
from lentra.services.property_service import PropertyService


class TelegramTelethonConnector:

    def __init__(self):

        self.api_id = int(os.getenv("TG_API_ID"))
        self.api_hash = os.getenv("TG_API_HASH")

        if not self.api_id or not self.api_hash:
            raise ValueError("TG_API_ID / TG_API_HASH not set")

        self.session = "lentra_telethon"

        self.client = TelegramClient(
            self.session,
            self.api_id,
            self.api_hash
        )

        self.pipeline = PropertyPipeline()
        self.service = PropertyService()

        # канал (можно менять)
        self.channel = "DomikoVietnam"

    async def start(self):

        await self.client.start()

        print("[TELETHON] started")

        @self.client.on(events.NewMessage(chats=self.channel))
        async def handler(event):

            text = event.message.message

            print("[INCOMING TELEGRAM CHANNEL]")
            print(text)

            result = self.pipeline.process_telegram_message({
                "text": text
            })

            normalized = result["property"]
            score = result["score"]

            saved = self.service.persist(
                normalized=normalized,
                score=score,
                raw=text
            )

            print(f"[SAVED] id={saved.id} score={score}")

        await self.client.run_until_disconnected()


if __name__ == "__main__":

    connector = TelegramTelethonConnector()

    asyncio.run(connector.start())
