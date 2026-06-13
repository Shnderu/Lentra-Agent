import asyncio
from telethon import TelegramClient, events
from lentra.services.ranking_service import get_feed

API_ID = 123
API_HASH = "xxx"

client = TelegramClient("bot", API_ID, API_HASH)


def format_item(i):
    return (
        f"{i['title']}\n"
        f"score: {i['score']}\n"
        f"price: {i['price_vnd_mln']}\n"
        f"area: {i['area_m2']}\n"
        "-------------------"
    )


@client.on(events.NewMessage(pattern="/feed"))
async def feed(event):
    items = get_feed(limit=10)

    if not items:
        await event.respond("No listings found")
        return

    text = "\n\n".join(format_item(i) for i in items)

    await event.respond(text)


async def main():
    print("[BOT] running ranking feed product")

    await client.start()
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
