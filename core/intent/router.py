
from core.intent.classifier import classify
from core.intent.registry import execute
from core.intent.policies import resolve
from core.fsm.context import get_state


async def route(user_id: int, text: str, source="message"):

    state = get_state(user_id)

    # 1. FSM override (самый высокий приоритет)
    if state != "idle":
        from core.fsm.manager import handle_message
        return await handle_message(user_id, text)

    # 2. classify intent
    intent = classify(text, source)

    # 3. execute by registry
    result = await execute(intent, user_id)

    return result
