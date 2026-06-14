from lentra.telegram.ux.router.init_router import router
from lentra.telegram.session.session_store import get_session, save_session
from lentra.telegram.session.navigation import push


def execute_callback(chat_id: int, callback_data: str):
    """
    Main agent loop entrypoint
    """

    session = get_session(chat_id)

    result = router.handle(callback_data, session)

    # update navigation stack if screen changes
    screen = result.get("screen")
    if screen:
        push(session["stack"], screen)

    session["data"].update(result.get("data", {}))

    save_session(chat_id, session)

    return result
