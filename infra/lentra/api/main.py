from fastapi import FastAPI
from lentra.runtime.bootstrap.main import get_gateway


def create_app() -> FastAPI:
    """
    SAFE ENTRYPOINT (v2)
    - NO engine imports
    - NO graph imports
    - ONLY gateway injection
    """

    app = FastAPI(title="Lentra API")

    gateway = get_gateway()

    @app.post("/search")
    async def search(payload: dict):
        return gateway.handle(payload)

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app
