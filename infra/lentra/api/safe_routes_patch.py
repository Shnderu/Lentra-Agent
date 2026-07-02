from fastapi import HTTPException


async def safe_search_handler(gateway, payload):
    try:
        return gateway.handle(payload)
    except Exception as e:
        return {
            "error": "gateway_failed",
            "message": str(e)
        }
