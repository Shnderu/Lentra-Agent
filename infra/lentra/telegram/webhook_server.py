from fastapi import FastAPI, Request
import os

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    return {"ok": True, "received": data}

@app.get("/health")
def health():
    return {"status": "ok"}
