from fastapi import FastAPI

from lentra.api.routes.search import router as search_router
from lentra.api.routes.admin import router as admin_router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(search_router)
    app.include_router(admin_router)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


# =========================
# CRITICAL FIX: ASGI ENTRYPOINT
# =========================

app = create_app()
