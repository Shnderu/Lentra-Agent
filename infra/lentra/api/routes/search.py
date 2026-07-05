from fastapi import APIRouter
from lentra.api.pipeline import get_pipeline
from lentra.api.response_builder import ResponseBuilder

router = APIRouter()


@router.post("/search")
def search(payload: dict):
    pipeline = get_pipeline()
    gateway = pipeline["gateway"]

    result = gateway.compute(payload)

    # HARD ENFORCEMENT: ONLY ONE RETURN PATH
    return ResponseBuilder.build(result)
