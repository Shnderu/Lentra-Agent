from fastapi import APIRouter, Request

router = APIRouter(prefix="/admin")


def get_gateway(request: Request):
    return request.app.state.gateway


@router.get("/health")
def health(request: Request):
    return get_gateway(request).watchdog.health()


@router.get("/engines")
def engines(request: Request):
    gw = get_gateway(request)
    return {
        "active": list(gw.isolator.engines.keys()),
        "total": len(gw.isolator.engines)
    }


@router.get("/state")
def state(request: Request):
    gw = get_gateway(request)
    return {
        "engines": list(gw.isolator.engines.keys()),
        "watchdog": gw.watchdog.health()
    }
