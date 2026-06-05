from fastapi import FastAPI
from core.db import init_db, fetch

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/flights")
async def flights():
    return await fetch("SELECT NOW()")
