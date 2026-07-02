from fastapi import FastAPI, Request
from lentra.runtime.control_panel.api import router as admin_router
from lentra.runtime.bootstrap.gateway_v3 import build_gateway_v3


def create_app() -> FastAPI:
    app = FastAPI()

    gateway = build_gateway_v3()

    app.state.gateway = gateway

    app.include_router(admin_router)

    @app.get("/health")
    def health(request: Request):
        return request.app.state.gateway.watchdog.health()

    @app.post("/search")
    async def search(payload: dict, request: Request):
        gw = request.app.state.gateway

        # V3 SAFE ROUTING
        if hasattr(gw, "engine_isolator"):
            return gw.engine_isolator.run_all(payload)

        return gw.handle(payload)

    return app
