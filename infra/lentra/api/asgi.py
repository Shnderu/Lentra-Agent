from fastapi import FastAPI, Request

from lentra.runtime.bootstrap.gateway_v3 import build_gateway_v3
from lentra.runtime.control_panel.api import router as admin_router


app = FastAPI()

gateway = build_gateway_v3()
app.state.gateway = gateway

app.include_router(admin_router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "gateway": gateway.engine_isolator is not None
    }


@app.post("/search")
async def search(payload: dict, request: Request):
    gw = request.app.state.gateway
    return gw.engine_isolator.run_all(payload)
