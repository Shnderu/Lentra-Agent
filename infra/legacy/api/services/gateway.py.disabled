# ============================================================
# API GATEWAY V17.2
# ============================================================

from lentra.core.product_router import ProductRouter


class GatewayService:
    def __init__(self):
        self.router = ProductRouter()

    async def handle(self, request: dict):
        return await self.router.handle(request)
