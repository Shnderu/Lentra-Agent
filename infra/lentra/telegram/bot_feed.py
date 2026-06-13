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
    price = f"{item['price_vnd_mln']} VND mln" if item.get("price_vnd_mln") else "no price"

    features = ", ".join(item.get("features", []))

    return (
        f"🏠 {item['title']}\n"
        f"📍 features: {features}\n"
        f"💰 {price}\n"
        f"⭐ score: {item.get('confidence', 0)}"
    )


@client.on(events.NewMessage(pattern="/feed"))
async def feed(event):
    items = ranking.get_feed(limit=10)

    # ----------------------------
    # CRITICAL FIX: empty guard
    # ----------------------------
    if not items:
        await event.respond("⚠️ No listings found")
        return

    text = "\n\n".join(format_item(i) for i in items if i)

    if not text.strip():
        await event.respond("⚠️ Empty feed result")
        return

    await event.respond(text)


@client.on(events.NewMessage(pattern="/search"))
async def search_handler(event):
    args = event.message.message.split()

    location = args[1] if len(args) > 1 else None
    ptype = args[2] if len(args) > 2 else None

    items = search.search(location=location, property_type=ptype)

    if not items:
        await event.respond("No results")
        return

    text = "\n\n".join(format_item(i) for i in items)

    await event.respond(text)


@client.on(events.NewMessage(pattern="/subscribe"))
async def subscribe(event):
    args = event.message.message.split()

    location = args[1] if len(args) > 1 else None
    max_price = None

    if len(args) > 2:
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
