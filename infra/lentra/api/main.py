from fastapi import FastAPI, Request

app = FastAPI()


# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}


# =========================
# TELEGRAM WEBHOOK ENTRY
# =========================
@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()

    # минимальный safe-лог
    print("[TELEGRAM UPDATE]", data)

    # TODO: сюда позже подключим:
    # - intent router
    # - market intelligence engine
    # - response generator

    return {
        "ok": True
    }
