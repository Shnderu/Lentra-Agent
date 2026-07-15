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
from lentra.core.market_intelligence.engines.dedup_engine import DedupEngine


API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")

SESSION = "lentra_source"

CHANNELS = [
    "danangrent",
]


USD_TO_VND = 25000


Base.metadata.create_all(bind=engine)


class TelegramRentalSource:


    def __init__(self):

        self.client = TelegramClient(
            SESSION,
            API_ID,
            API_HASH
        )

        self.parser = RentalParser()

        self.dedup_engine = DedupEngine()



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


            if existing:

                print(
                    "[RAW EXISTS]",
                    message.id
                )


            else:

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


            parsed = self.parser.parse(
                message.text
            )


            price_vnd_mln = (
                parsed.get("price_vnd_mln")
            )


            if not price_vnd_mln and parsed.get("price_usd"):

                price_vnd_mln = (
                    parsed["price_usd"]
                    * USD_TO_VND
                    / 1000000
                )


            existing_apartment = (
                db.query(Apartment)
                .filter(
                    Apartment.source_chat_id == message.chat_id,
                    Apartment.source_message_id == message.id
                )
                .first()
            )

            if existing_apartment:
                print(
                    "[APARTMENT EXISTS]",
                    message.id
                )
                return


            prop = Apartment(

                title=message.text[:200],

                price_vnd_mln=price_vnd_mln,

                city=(
                    parsed.get("city")
                    or "da_nang"
                ),

                district=(
                    parsed.get("district")
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

                # normalized fields

                area_m2=parsed.get("area_m2"),

                deposit_vnd_mln=parsed.get("deposit"),

                electricity_price=parsed.get("electricity_price"),

                water_price=parsed.get("water_price"),

                floor=parsed.get("floor"),

                total_floors=parsed.get("total_floors"),

                balcony=bool(
                    parsed.get("balcony", False)
                ),

                parking=bool(
                    parsed.get("parking", False)
                ),

                wifi=bool(
                    parsed.get("wifi", False)
                ),

                internet=bool(
                    parsed.get("internet", False)
                ),

                air_conditioner=bool(
                    parsed.get("air_conditioner", False)
                ),

                washing_machine=bool(
                    parsed.get("washing_machine", False)
                ),

                kitchen=bool(
                    parsed.get("kitchen", False)
                ),

                refrigerator=bool(
                    parsed.get("refrigerator", False)
                ),

                furnished=bool(
                    parsed.get("furnished", False)
                ),

                property_type=parsed.get("type"),

                currency=(
                    "USD"
                    if parsed.get("price_usd")
                    else "VND"
                ),

                description=message.text,

                raw_text=message.text,

                features=parsed.get("features"),

                score=0.5,

                source_chat_id=message.chat_id,

                source_message_id=message.id

            )


            db.add(prop)

            db.commit()

            dedup_result = self.dedup_engine.evaluate(
                {
                    "id": prop.id,
                    "title": prop.title,
                    "city": prop.city,
                    "type": prop.property_type,
                    "price": prop.price_vnd_mln,
                    "district": prop.district,
                    "features": prop.features,
                    "source": {
                        "chat_id": prop.source_chat_id,
                        "message_id": prop.source_message_id
                    }
                }
            )

            print(
                "[DEDUP]",
                dedup_result.get("dedup")
            )


            print(
                "[APARTMENT INGESTED]",
                prop.title[:60]
            )


        finally:

            db.close()



if __name__ == "__main__":

    asyncio.run(
        TelegramRentalSource().run()
    )
