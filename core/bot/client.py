import os
import aiohttp

BOT_TOKEN = os.getenv("BOT_TOKEN")

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


async def send_message(chat_id: int, text: str):

    if not BOT_TOKEN:
        print("[BOT] missing token")
        return

    async with aiohttp.ClientSession() as session:
        await session.post(
            f"{API_URL}/sendMessage",
            data={
                "chat_id": chat_id,
                "text": text
            }
        )
