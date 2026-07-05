from fastapi import FastAPI

def patch_app(app: FastAPI):
    # disable any accidental streaming fallback
    app.state._force_single_response = True
    return app
