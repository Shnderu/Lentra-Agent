from app.core.gateway.flow_glue import FlowGlue


class ExecutionEntryV1:
    """
    Single canonical entrypoint for ALL runtime flows.

    API / BOT / WORKER MUST eventually call only this.
    """

    def __init__(self, intent_router, scenario_engine):
        self.glue = FlowGlue(intent_router, scenario_engine)

    def handle(self, payload: dict) -> dict:
        """
        Unified execution contract:
        input  -> normalized event
        output -> scenario result
        """

        if not isinstance(payload, dict):
            return {
                "ok": False,
                "error": "invalid_payload_type"
            }

        return self.glue.resolve(payload)


# singleton entry (freeze model)
entrypoint = None


def init(intent_router, scenario_engine):
    global entrypoint
    entrypoint = ExecutionEntryV1(intent_router, scenario_engine)


def execute(payload: dict) -> dict:
    if entrypoint is None:
        return {
            "ok": False,
            "error": "execution_entry_not_initialized"
        }

    return entrypoint.handle(payload)
