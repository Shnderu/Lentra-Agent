from fastapi import APIRouter
from lentra.runtime.control_panel.api import get_control_state, health

router = APIRouter()

@router.get("/control/state")
def state():
    return get_control_state()

@router.get("/control/health")
def h():
    return health()
