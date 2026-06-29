from fastapi import FastAPI
from fastapi.responses import JSONResponse
import traceback

from lentra.services.intelligence import handle_request

app = FastAPI()


@app.post("/search")
def search(payload: dict):
    try:
        return handle_request(payload)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "trace": traceback.format_exc()
            }
        )
