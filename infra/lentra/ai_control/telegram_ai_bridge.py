"""
Telegram → AI Control Layer bridge
Все сообщения переводятся в TaskRouter.
"""

from .task_router import TaskRouter


class TelegramAIBridge:

    def __init__(self):
        self.router = TaskRouter()

    def handle_message(self, message_text: str, context_files=None):
        """
        Главная точка входа из Telegram bot handler.
        """

        task = message_text.strip()

        result = self.router.route(
            task=task,
            context_files=context_files or []
        )

        return self._format_response(result)

    def _format_response(self, result: dict) -> str:
        """
        Формат ответа для Telegram.
        """

        if result.get("status") != "ok":
            return f"❌ ERROR: {result.get('result')}"

        return f"✅ AI TASK DONE\n\n{result.get('result')}"
