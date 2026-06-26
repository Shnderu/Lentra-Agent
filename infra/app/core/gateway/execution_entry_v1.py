import traceback
from app.core.gateway.flow_glue import FlowGlue


class ExecutionEntryV1:

    def __init__(self, intent_router, scenario_engine):

        try:
            print("[ENTRY] INIT START")

            print("[ENTRY] intent_router =", intent_router)
            print("[ENTRY] scenario_engine =", scenario_engine)

            self.glue = FlowGlue(intent_router, scenario_engine)

            print("[ENTRY] FLOWGLUE OK")

        except Exception as e:
            print("[ENTRY] INIT FAILED:", str(e))
            traceback.print_exc()
            raise


    def handle(self, payload: dict) -> dict:

        if not isinstance(payload, dict):
            return {"ok": False, "error": "invalid_payload_type"}

        try:
            return self.glue.resolve(payload)
        except Exception as e:
            traceback.print_exc()
            return {
                "ok": False,
                "error": "execution_entry_runtime_failed",
                "details": str(e)
            }


entrypoint = None


def init(intent_router, scenario_engine):
    global entrypoint

    try:
        print("[ENTRY] GLOBAL INIT START")

        entrypoint = ExecutionEntryV1(intent_router, scenario_engine)

        print("[ENTRY] GLOBAL INIT OK")

    except Exception as e:
        print("[ENTRY] GLOBAL INIT FAILED:", str(e))
        traceback.print_exc()
        entrypoint = None


def execute(payload: dict) -> dict:

    if entrypoint is None:
        return {
            "ok": False,
            "error": "execution_entry_not_initialized"
        }

    return entrypoint.handle(payload)
