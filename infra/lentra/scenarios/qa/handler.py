def handle(flow, params=None):
    return {
        "status": "ok",
        "scenario": "qa",
        "answer": f"processed question: {flow.text}"
    }
