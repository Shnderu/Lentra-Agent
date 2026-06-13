import os
import asyncio

from telethon import TelegramClient, events

from lentra.services.ranking_service import RankingService
from lentra.services.search_service import SearchService
from lentra.services.alert_service import AlertService


API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

client = TelegramClient("lentra_bot", API_ID, API_HASH)

ranking = RankingService()
search = SearchService()
alerts = AlertService()


def format_item(item):
    price = f"{item['price']} {item['currency']}" if item["price"] else "no price"

    return (
        f"🏠 {item['type']}\n"
        f"📍 {item['location']}\n"
        f"💰 {price}\n"
        f"⭐ {item['confidence']}\n\n"
        f"{item['description'][:200]}"
    )


# ----------------------------
# FEED
# ----------------------------
@client.on(events.NewMessage(pattern="/feed"))
async def feed(event):
    items = ranking.get_feed(limit=10)
    await event.respond("\n\n".join(format_item(i) for i in items))


# ----------------------------
# SEARCH (NEW)
# ----------------------------
@client.on(events.NewMessage(pattern="/search"))
async def search_handler(event):
    args = event.message.message.split()

    location = None
    max_price = None
    min_price = None
    ptype = None

    # /search danang apartment 500
    if len(args) >= 2:
        location = args[1]

    if len(args) >= 3:
        ptype = args[2]

    if len(args) >= 4:
        try:
            max_price = float(args[3])
        except:
            pass

    items = search.search(
        location=location,
        property_type=ptype,
        max_price=max_price
    )

    if not items:
        await event.respond("No results.")
        return

    await event.respond("\n\n".join(format_item(i) for i in items))


# ----------------------------
# SUBSCRIBE (alerts)
# ----------------------------
@client.on(events.NewMessage(pattern="/subscribe"))
async def subscribe(event):
    args = event.message.message.split()

    location = args[1] if len(args) >= 2 else None
    max_price = None

    if len(args) >= 3:
        try:
            max_price = float(args[2])
        except:
            pass

    alerts.create_alert(
        chat_id=event.chat_id,
        location=location,
        max_price=max_price
    )

    await event.respond("✅ Alert created")


async def main():
    print("[BOT] running feed + search + alerts")

    await client.start(bot_token=BOT_TOKEN)

    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
