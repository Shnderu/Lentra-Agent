from fastapi import FastAPI
from app.core.gateway.execution_entry_v1 import execute as gateway_execute

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/execute")
async def execute(payload: dict):
    """
    Единственная точка входа API → core gateway
    """
    return gateway_execute(payload)
