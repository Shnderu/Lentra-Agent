from fastapi import APIRouter

router = APIRouter(prefix="/admin")

@router.get("/engines")
def engines():
    return {"status": "ok"}

@router.get("/debug")
def debug():
    return {
        "loaded": True,
        "module": __name__
    }
