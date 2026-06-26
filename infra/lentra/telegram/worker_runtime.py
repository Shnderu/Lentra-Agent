from lentra.workers.base_worker import BaseWorker


class TelegramWorker(BaseWorker):
    """
    Telegram runtime MUST NOT bypass executor
    """

    def on_message(self, message: dict):
        task = {
            "type": "telegram_message",
            "payload": message
        }

        return self.handle(task)
