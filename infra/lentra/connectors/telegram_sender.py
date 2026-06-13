def send_message(bot_api, chat_id, text):
    bot_api.send_message(
        chat_id=chat_id,
        text=text
    )
