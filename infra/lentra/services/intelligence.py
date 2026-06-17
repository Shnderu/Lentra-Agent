from lentra.core.contracts.dto import RequestDTO, ResponseDTO
from lentra.core.context.runtime_context import create_context
from lentra.services.pipeline_definition import build_pipeline


def handle_request(payload: dict):

    ctx = create_context(user_id=payload.get("user_id"))

    req = RequestDTO(
        query=payload.get("query"),
        user_id=payload.get("user_id"),
        context=payload
    )

    pipeline = build_pipeline()

    result = pipeline.execute(
        context=ctx,
        input_data={"query": req.query}
    )

    return ResponseDTO(
        query=req.query,
        results=result,
        meta={
            "request_id": ctx.request_id,
            "sealed": True
        }
    ).__dict__
