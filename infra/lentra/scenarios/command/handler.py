def handle(flow, params=None):
    return {
        "status": "ok",
        "scenario": "command",
        "action": f"executed command: {flow.text}"
    }
