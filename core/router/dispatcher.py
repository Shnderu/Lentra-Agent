from core.queue.queue import enqueue


class Dispatcher:

    def dispatch(self, intent_result):

        intent = intent_result.intent

        if intent == "unknown":
            return {
                "action": "reply",
                "text": "Не понял запрос"
            }

        task_id = enqueue(intent, intent_result.payload)

        return {
            "action": "queue",
            "task_id": task_id,
            "type": intent
        }
