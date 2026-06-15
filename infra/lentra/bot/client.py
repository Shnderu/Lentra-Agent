import httpx


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def post(self, path: str, payload: dict):
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(f"{self.base_url}{path}", json=payload)
            resp.raise_for_status()
            return resp.json()
