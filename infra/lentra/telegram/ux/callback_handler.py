from lentra.telegram.state.machine import next_state
from lentra.telegram.intent.router import detect_intent
from lentra.telegram.intent.mapper import map_intent_to_task


def handle_callback(callback_data, user_id, task_id):

    state = next_state(user_id, callback_data, {"task_id": task_id})

    intent = detect_intent(state, {"task_id": task_id}, callback_data)

    return map_intent_to_task(intent, user_id, {"task_id": task_id})
