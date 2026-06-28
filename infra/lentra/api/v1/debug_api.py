from fastapi import APIRouter
from lentra.core.pipeline.pipeline import LentraPipeline

router = APIRouter()

@router.get("/debug")
def debug(q: str = "test"):
    p = LentraPipeline()

    try:
        ctx = p.run({"title": q})

        return {
            "ok": True,
            "type": str(type(ctx)),
            "has_snapshot": hasattr(ctx, "snapshot"),
            "ctx": str(ctx)
        }

    except Exception as e:
        return {
            "ok": False,
            "error": str(e)
        }
