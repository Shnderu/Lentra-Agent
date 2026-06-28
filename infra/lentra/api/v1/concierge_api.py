from fastapi import APIRouter
from lentra.core.pipeline.pipeline import LentraPipeline

router = APIRouter()
pipeline = LentraPipeline()


@router.get("/search")
def search(q: str):
    ctx = pipeline.run({"title": q})

    return {
        "query": ctx.get("query"),
        "total": ctx.get("total", 0),
        "objects": ctx.get("objects", [])
    }


from fastapi import FastAPI

app = FastAPI()
app.include_router(router)
