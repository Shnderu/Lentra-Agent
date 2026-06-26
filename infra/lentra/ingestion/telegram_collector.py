import time
import random
from lentra.core.queue.task_repository import TaskRepository
from lentra.ingestion.parsers.rental_parser import RentalParser


DSN = "postgresql://lentra:lentra@localhost:5432/lentra"


class TelegramCollector:

    def __init__(self):
        self.repo = TaskRepository(DSN)
        self.parser = RentalParser()

        self.mock_messages = [
            "studio apartment near beach 700$ da nang",
            "cheap room bangkok 300$ internet good",
            "modern condo chiang mai 900$",
            "small studio bali 500$ expat friendly",
            "apartment sea view da nang 1200$"
        ]

    def run(self):
        print("[INGESTION] TELEGRAM COLLECTOR STARTED")

        while True:
            msg = random.choice(self.mock_messages)

            parsed = self.parser.parse(msg)

            payload = {
                "text": msg,
                "parsed": parsed,
                "source": "telegram_mock",
                "timestamp": time.time()
            }

            task_id = self.repo.push(payload)

            print(f"[INGESTED] task_id={task_id} parsed={parsed}")

            time.sleep(3)


if __name__ == "__main__":
    TelegramCollector().run()
