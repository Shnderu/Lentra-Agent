from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/health")
def health(request: Request):
    return request.app.state.gateway.watchdog.health()
