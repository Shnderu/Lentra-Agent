from fastapi import APIRouter
from api.routes.task import router as task_router
from api.routes.metrics import router as metrics_router

router = APIRouter()

router.include_router(task_router)
router.include_router(metrics_router)
