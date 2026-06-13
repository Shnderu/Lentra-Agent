"""
Lentra Observability API v12b
Control-plane read interface (NO EXECUTION)
"""

from fastapi import FastAPI
from core.observability.system_observer_v12a import SystemObserver

app = FastAPI(title="Lentra Observability v12b")

observer = SystemObserver()


@app.post("/snapshot")
def snapshot(event: dict):
    return observer.snapshot(event)


@app.get("/health")
def health():
    return {
        "status": "OK",
        "mode": "OBSERVABILITY_V12B"
    }


@app.get("/risk")
def risk(event: dict):
    data = observer.snapshot(event)
    return data.get("prediction_v9", {})


@app.get("/incidents")
def incidents(event: dict):
    data = observer.snapshot(event)
    return data.get("fusion_v7", {})


@app.get("/decisions")
def decisions(event: dict):
    data = observer.snapshot(event)
    return data.get("control_v10", {})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8090)
