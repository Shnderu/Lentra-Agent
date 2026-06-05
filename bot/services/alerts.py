import asyncio
from bot.workers.alert_worker import run_worker


def start_alert_engine():
    asyncio.create_task(run_worker())
