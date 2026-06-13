import os
import io
import qrcode
import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from telethon import TelegramClient

app = FastAPI()

api_id = int(os.getenv("TG_API_ID"))
api_hash = os.getenv("TG_API_HASH")

client = TelegramClient("lentra_qr", api_id, api_hash)

qr_login_state = {"qr": None, "task": None}


@app.get("/auth/qr")
async def get_qr():
    await client.connect()

    if await client.is_user_authorized():
        return {"status": "already_authorized"}

    qr_login = await client.qr_login()

    qr_login_state["qr"] = qr_login

    img = qrcode.make(qr_login.url)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")


@app.get("/auth/qr/status")
async def qr_status():
    if not qr_login_state["qr"]:
        return {"status": "no_qr"}

    return {"status": "waiting_scan"}


@app.get("/auth/qr/wait")
async def qr_wait():
    if not qr_login_state["qr"]:
        return JSONResponse({"error": "no qr generated"}, status_code=400)

    qr = qr_login_state["qr"]

    await qr.wait()

    me = await client.get_me()

    return {
        "status": "logged_in",
        "user_id": me.id,
        "username": me.username
    }


@app.on_event("shutdown")
async def shutdown():
    await client.disconnect()
