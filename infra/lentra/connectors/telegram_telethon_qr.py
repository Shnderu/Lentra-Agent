import os
import asyncio
import qrcode

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.auth import ExportLoginTokenRequest, ImportLoginTokenRequest


API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")


async def main():

    client = TelegramClient(StringSession(), API_ID, API_HASH)
    await client.connect()

    # получаем login token
    res = await client(ExportLoginTokenRequest(
        api_id=API_ID,
        api_hash=API_HASH,
        except_ids=[]
    ))

    token = res.token

    # ❗ ВАЖНО: QR должен быть самим токеном, не tg://
    qr_path = "/tmp/telegram_qr.png"

    img = qrcode.make(token)
    img.save(qr_path)

    print("\nOPEN THIS QR ON PHONE:\n")
    print(qr_path)

    print("\nTelegram → Settings → Devices → Link Device → Scan QR")

    # polling login
    while True:
        try:
            await client(ImportLoginTokenRequest(token=token))
            print("\nLOGIN SUCCESS")
            break
        except Exception:
            pass

        await asyncio.sleep(2)

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
