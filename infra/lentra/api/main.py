import uvicorn

from fastapi import FastAPI

from lentra.api.app_patch import patch_app
from lentra.api.routes.search import router as search_router


def create_app() -> FastAPI:

    app = FastAPI(
        title="Lentra AI Market Intelligence API"
    )

    app = patch_app(app)

    app.include_router(
        search_router
    )

    @app.get("/health")
    def health():
        return {
            "status": "ok"
        }

    return app


app = create_app()


def main():
    print("[API] starting uvicorn")

    uvicorn.run(
        "lentra.api.main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )


if __name__ == "__main__":
    main()
