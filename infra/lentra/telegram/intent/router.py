from lentra.api.pipeline import run_pipeline

from lentra.telegram.router.intent_router import IntentRouter


_intent_router = IntentRouter()


def route(event):

    """
    Telegram transport adapter.

    Search execution goes through canonical API pipeline.
    """

    event_type = event.get(
        "type"
    )

    if event_type == "search":

        payload = event.get(
            "payload",
            {}
        )

        result = run_pipeline(
            payload
        )

        return {
            "screen": "search_results",
            "state": result
        }


    return {
        "ok": True,
        "type": "noop"
    }



def detect_intent(
    state,
    payload,
    callback_data
):
    """
    Compatibility adapter for callback layer.

    Callback layer historically imported this function.
    Intent detection is delegated to canonical telegram router.
    """

    text = (
        callback_data
        or ""
    )

    return _intent_router.detect(
        text
    )
