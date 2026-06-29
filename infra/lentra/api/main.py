from fastapi import FastAPI
from lentra.services.intelligence import handle_request

app = FastAPI()

@app.post("/search")
def search(payload: dict):
    print("[SEARCH INPUT]", payload)

    try:
        result = handle_request(payload)
        print("[SEARCH OUTPUT]", result)
        return result
    except Exception as e:
        print("[SEARCH ERROR]", repr(e))
        return {
            "error": str(e)
        }
