from fastapi import FastAPI
from lentra.runtime.bootstrap.wiring_safe import build_gateway

app = FastAPI()

gateway = build_gateway()

@app.get("/health")
def health():
    return {"status": "ok", "mode": "gateway_connected"}

@app.post("/search")
def search(payload: dict):
    print("=== SEARCH HIT ===")
    print(payload)

    try:
        result = gateway["handle"](payload)
        print("=== RESULT ===", result)
        return result
    except Exception as e:
        import traceback
        print("=== ERROR ===")
        traceback.print_exc()
        return {
            "status": "error",
            "error": str(e)
        }
