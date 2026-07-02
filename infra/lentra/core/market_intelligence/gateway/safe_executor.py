import traceback


def safe_execute(engine, payload):
    try:
        return engine.evaluate(payload)
    except Exception as e:
        return {
            "error": "engine_failed",
            "message": str(e),
            "trace": traceback.format_exc()
        }
