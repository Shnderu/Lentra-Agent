from bot.cache import get_cache, set_cache
import asyncio
import logging

logger = logging.getLogger(__name__)


async def alert_engine():
    while True:
        try:
            data = get_cache("flight_prices")

            if not data:
                await asyncio.sleep(10)
                continue

            # пример логики алертов
            for item in data:
                price = item.get("price")
                target = item.get("target_price")

                if price and target and price <= target:
                    logger.info(f"ALERT TRIGGERED: {item}")

            await asyncio.sleep(30)

        except Exception as e:
            logger.error(f"Alert engine error: {e}")
            await asyncio.sleep(10)
