from lentra.services.pipeline_definition import pipeline


def handle_request(intent: dict):
    """
    Единая точка входа для search API
    """

    # защита от неправильной инъекции pipeline
    if not hasattr(pipeline, "execute"):
        raise RuntimeError(
            f"[INTELLIGENCE ERROR] pipeline is invalid: {type(pipeline)}"
        )

    result = pipeline.execute(intent)

    return result
