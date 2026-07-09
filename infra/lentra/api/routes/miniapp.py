from fastapi import APIRouter

from lentra.api.pipeline import run_pipeline

from lentra.api.schemas.miniapp import (
    MiniAppSearchResponseSchema
)

from lentra.api.schemas.miniapp_object import (
    MiniAppObjectDetailResponseSchema
)


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

        "contract_version": "miniapp.v1",

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


@router.get(
    "/object/{object_id}",
    response_model=MiniAppObjectDetailResponseSchema
)
def miniapp_object_detail(
    object_id: str
):

    result = run_pipeline(
        {
            "query": object_id
        }
    )


    for item in result.get(
        "results",
        []
    ):

        if item.get(
            "id"
        ) == object_id:

            mini_app = item.get(
                "mini_app",
                {}
            )


            return {

                "contract_version":
                    "miniapp.v1",

                "object":
                    mini_app.get(
                        "object",
                        {}
                    ),

                "intelligence":
                    mini_app.get(
                        "intelligence",
                        {}
                    ),

                "verdict":
                    mini_app.get(
                        "verdict",
                        {}
                    ),

                "explanation":
                    mini_app.get(
                        "explanation",
                        {}
                    )

            }


    return {

        "contract_version":
            "miniapp.v1",

        "object":
            {},

        "intelligence":
            {},

        "verdict":
            {},

        "explanation":
            {}

    }
