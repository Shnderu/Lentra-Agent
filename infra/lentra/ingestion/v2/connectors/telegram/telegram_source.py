import os
import asyncio

from telethon import TelegramClient

from lentra.storage.models import RawMessageDB
from lentra.models.apartment import Apartment

from lentra.db.session import (
    SessionLocal,
    engine,
    Base
)

from lentra.ingestion.parsers.rental_parser import RentalParser


API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")


SESSION = "lentra_source"


CHANNELS = [
    "danangrent",
]


Base.metadata.create_all(bind=engine)


class TelegramRentalSource:


    def __init__(self):

        self.client = TelegramClient(
            SESSION,
            API_ID,
            API_HASH
        )

        self.parser = RentalParser()



    async def run(self):

        await self.client.start()

        print(
            "[TELEGRAM SOURCE] started"
        )


        for channel in CHANNELS:

            entity = await self.client.get_entity(
                channel
            )


            async for message in self.client.iter_messages(
                entity,
                limit=50
            ):

                if not message.text:
                    continue


                self.process_message(
                    message,
                    channel
                )



        await self.client.disconnect()



    def process_message(
        self,
        message,
        channel
    ):

        db = SessionLocal()

        try:

            existing = (
                db.query(RawMessageDB)
                .filter(
                    RawMessageDB.message_id == message.id,
                    RawMessageDB.chat_id == message.chat_id
                )
                .first()
            )


            if not existing:

                raw = RawMessageDB(

                    message_id=message.id,

                    chat_id=message.chat_id,

                    chat_title=channel,

                    text=message.text,

                    raw_json={
                        "date":
                            str(message.date)
                    }

                )


                db.add(raw)

                db.commit()

                print(
                    "[RAW INGESTED]",
                    message.id
                )

            else:

                print(
                    "[RAW EXISTS]",
                    message.id
                )


            parsed = self.parser.parse(
                message.text
            )


            prop = Apartment(

                title=message.text[:200],

                price_vnd_mln=(
                    parsed.get("price_vnd_mln")
                    or parsed.get("price")
                ),

                city=(
                    parsed.get("city")
                    or "da_nang"
                ),

                district=(
                    parsed.get("district")
                    or parsed.get("location")
                ),

                bedrooms=parsed.get("bedrooms"),

                bathrooms=parsed.get("bathrooms"),

                pool=bool(
                    parsed.get("pool", False)
                ),

                sea_view=bool(
                    parsed.get("sea_view", False)
                ),

                pet_friendly=bool(
                    parsed.get("pet_friendly", False)
                ),

                score=0.5

            )


            db.add(prop)

            db.commit()


            print(
                "[APARTMENT INGESTED]",
                prop.title[:50]
            )


        finally:

            db.close()



if __name__ == "__main__":

    asyncio.run(
        TelegramRentalSource().run()
    )
