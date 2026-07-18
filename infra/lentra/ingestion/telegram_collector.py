import time
import random

from lentra.ingestion.task_writer import TaskWriter
from lentra.ingestion.parsers.rental_parser import RentalParser


class TelegramCollector:

    def __init__(self):
        self.repo = TaskWriter()
        self.parser = RentalParser()

        self.mock_messages = [
            "studio apartment near beach 700$ da nang",
            "cheap room bangkok 300$ internet good",
            "modern condo chiang mai 900$",
            "small studio bali 500$ expat friendly",
            "apartment sea view da nang 1200$"
        ]


    def run(self):

        print(
            "[INGESTION] TELEGRAM COLLECTOR STARTED",
            flush=True
        )


        while True:

            msg = random.choice(
                self.mock_messages
            )


            parsed = self.parser.parse(
                msg
            )


            payload = {
                "query": msg,

                "listing": parsed,

                "source": "telegram_mock",

                "timestamp": time.time(),

                # backward compatibility
                "text": msg,
                "parsed": parsed
            }


            task_id = self.repo.push(
                payload
            )


            print(
                f"[INGESTED] task_id={task_id} query={msg} parsed={parsed}",
                flush=True
            )


            time.sleep(3)



if __name__ == "__main__":

    TelegramCollector().run()
