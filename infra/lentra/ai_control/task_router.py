"""
Lentra AI Control Layer - Task Router
Маршрутизатор задач от бота / CLI в Aider Gateway.
"""

from .aider_gateway import AiderGateway


class TaskRouter:
    """
    Принимает задачи от Telegram bot / API
    и отправляет их в AI gateway.
    """

    def __init__(self):
        self.gateway = AiderGateway()

    def route(self, task: str, context_files: list[str] = None):
        """
        Основной вход.
        """

        # минимальная нормализация
        task = task.strip()

        # маршрутизация в AI слой
        result = self.gateway.run_task(
            task=task,
            files=context_files or []
        )

        return {
            "status": "ok",
            "result": result
        }


# CLI test
if __name__ == "__main__":
    router = TaskRouter()
    response = router.route("fix duplicate detection logic")
    print(response)
