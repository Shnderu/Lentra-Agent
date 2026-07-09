from fastapi import APIRouter

from lentra.api.pipeline import run_pipeline
from lentra.api.schemas.miniapp import MiniAppSearchResponseSchema


router = APIRouter(
    prefix="/api/miniapp",
    tags=["miniapp"]
)


@router.post(
    "/search",
    response_model=MiniAppSearchResponseSchema
)
def miniapp_search(
    payload: dict
):

    result = run_pipeline(
        payload
    )

    return {

        "api_version": "1.0",

        "schema_version": "3.1",

        "platform": "telegram_mini_app",

        "query": result.get(
            "query",
            ""
        ),

        "count": result.get(
            "count",
            0
        ),

        "results": [

            item.get(
                "mini_app",
                {}
            )

            for item in result.get(
                "results",
                []
            )

        ]

    }
