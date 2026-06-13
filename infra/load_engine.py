# LENTRA LOAD ENGINE MVP

import asyncio
from pyrogram import Client

API_ID = 34837463
API_HASH = "660e4e614f3ebc98d02284ef4cffec19"

CLIENT_NAME = "lentra_pyro"

TOTAL_MESSAGES = 50
DELAY = 0.2  # seconds between messages

async def main():
    app = Client(CLIENT_NAME, api_id=API_ID, api_hash=API_HASH)

    await app.start()

    print("[LOAD] START")

    sent = 0

    for i in range(TOTAL_MESSAGES):
        msg = f"LOAD_TEST_{i}"
        await app.send_message("me", msg)
        print(f"[LOAD] SENT {msg}")
        sent += 1
        await asyncio.sleep(DELAY)

    await app.stop()

    print(f"[LOAD] DONE sent={sent}")

if __name__ == "__main__":
    asyncio.run(main())
