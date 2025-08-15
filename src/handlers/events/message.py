from ...config import WATCH_USER_ID, SOURCE_CHANNEL_ID, DEST_CHANNEL_ID

_seen_event_ids = set()

def handle_message(body, event, say, client, logger):
    event_id = body.get("event_id")
    if event_id in _seen_event_ids:
        return
    _seen_event_ids.add(event_id)

    channel = event.get("channel")
    if channel != SOURCE_CHANNEL_ID:
        return

    if event.get("subtype") or event.get("bot_id"):
        return

    text = event.get("text", "") or ""
    mention_token = f"<@{WATCH_USER_ID}>"
    if mention_token not in text:
        return

    user_who_mentioned = event.get("user")
    permalink = client.chat_getPermalink(channel=channel, message_ts=event.get("ts")).get("permalink")

    client.chat_postMessage(
        channel=DEST_CHANNEL_ID,
        text=(
            f"🔔 Hey <@{WATCH_USER_ID}>, te mencionaron en <#{SOURCE_CHANNEL_ID}>.\n"
            f"Quien: <@{user_who_mentioned}>\n"
            f"Mensaje: {text}\n"
            f"Link: {permalink}"
        )
    )

# TODO: quizá la sola mención puede enviar lista de comandos en ephemeral
# def handle_app_mention(body, say):
#     user = body["event"]["user"]
#     say(f"Pong <@{user}> 🏓")
