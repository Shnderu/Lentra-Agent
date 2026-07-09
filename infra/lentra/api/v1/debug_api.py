from fastapi import APIRouter

from lentra.core.pipeline.canonical_search_pipeline import (
    CanonicalSearchPipeline
)

from lentra.core.pipeline.canonical_entrypoint import (
    CanonicalSearchEntrypoint
)

from lentra.core.pipeline.search_pipeline import (
    SearchPipeline
)


router = APIRouter()



@router.get("/debug")
def debug(
    q: str = "test"
):

    pipeline = CanonicalSearchPipeline(
        SearchPipeline()
    )


    entrypoint = CanonicalSearchEntrypoint(
        pipeline
    )


    try:

        result = entrypoint.execute(
            {
                "query": q,
                "objects": []
            }
        )


        return {

            "ok": True,

            "pipeline":
                "canonical_search_pipeline",

            "result":
                result

        }


    except Exception as e:


        return {

            "ok": False,

            "error":
                str(e)

        }
