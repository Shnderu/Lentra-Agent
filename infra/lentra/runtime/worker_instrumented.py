from lentra.runtime.execution.instrumentation import RuntimeInstrument

instrument = RuntimeInstrument()


def execute_task(task_id: str, payload: dict):
    instrument.start_task(task_id)

    # placeholder execution
    result = {"ok": True}

    instrument.end_task(task_id)

    return result
