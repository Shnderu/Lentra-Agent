from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/debug/engines")
async def engines_debug(request: Request):
    gateway = request.app.state.gateway

    # unwrap if needed
    if hasattr(gateway, "gateway"):
        gw = gateway.gateway
    else:
        gw = gateway

    engines = getattr(gw, "engines", {})

    return {
        "engines": list(engines.keys()),
        "status": "ok"
    }
