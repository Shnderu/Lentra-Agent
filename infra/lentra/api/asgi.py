from fastapi import FastAPI, Request

from lentra.runtime.bootstrap.gateway_v3 import build_gateway_v3
from lentra.runtime.control_panel.api import router as admin_router
from lentra.core.market_intelligence.decision_layer import DecisionLayer


app = FastAPI()

gateway = build_gateway_v3()
decision_layer = DecisionLayer()

app.state.gateway = gateway
app.state.decision_layer = decision_layer

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

    result = gw.engine_isolator.run_all(payload)

    # FINAL LAYER (Decision OS)
    result["decision"] = request.app.state.decision_layer.evaluate(result)

    return result
