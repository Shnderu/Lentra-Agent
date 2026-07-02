import uvicorn

from lentra.runtime.bootstrap.wiring import build_gateway


def main():
    gateway = build_gateway()

    # SAFE FALLBACK: gateway MUST expose app OR create it
    app = gateway.build_app() if hasattr(gateway, "build_app") else gateway

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    main()
