from fastapi import FastAPI
from lentra.services.intelligence import handle_request


def create_app():
    app = FastAPI()

    @app.post("/search")
    def search(payload: dict):
        return handle_request(payload)

    return app
