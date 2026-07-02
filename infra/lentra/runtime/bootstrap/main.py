from lentra.runtime.bootstrap.wiring_safe import build_gateway
from lentra.api.main import create_app

app = None
gateway = None

def bootstrap():
    global app, gateway

    gateway = build_gateway()
    app = create_app()
    app.state.gateway = gateway

    return app

app = bootstrap()
