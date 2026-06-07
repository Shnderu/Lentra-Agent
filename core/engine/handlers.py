from core.engine.router import router


@router.register("test")
def handle_test(task: dict):
    print(f"[HANDLER:test] payload={task['payload']}")
    return {"ok": True}


@router.register("flight_search")
def handle_flight_search(task: dict):
    print("[HANDLER:flight_search] TODO implement search pipeline")
    return {"ok": True}
