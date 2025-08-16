from ...config import TEAM_ID, SOURCE_CHANNEL_IDS, DEST_CHANNEL_IDS
from ...db import get_current, next_turn

_seen_event_ids = set()


def handle_message(body, event, client):
    event_id = body.get("event_id")
    if event_id in _seen_event_ids:
        return
    _seen_event_ids.add(event_id)

    print(event)
    channel = event.get("channel")
    if channel not in SOURCE_CHANNEL_IDS:
        return

    if event.get("subtype") or event.get("bot_id"):
        return

    text = event.get("text", "") or ""
    mention_token = f"<!subteam^{TEAM_ID}>"
    if mention_token not in text:
        return

    permalink = client.chat_getPermalink(channel=channel, message_ts=event.get("ts")).get("permalink")

    support_member = get_current()

    if not support_member:
        support_member = next_turn()

    if not support_member:
        for dest_chan in DEST_CHANNEL_IDS:
            client.chat_postMessage(
                channel=dest_chan,
                text=(
                    f"🔔 Hey <!subteam^{TEAM_ID}>, nos mencionaronen <#{channel}> y no hay turno asignado\n"
                    f"Link: {permalink}"
                )
            )
        return

    for dest_chan in DEST_CHANNEL_IDS:
        client.chat_postMessage(
            channel=dest_chan,
            text=(
                f"🔔 Hey <@{support_member['slack_user_id']}>, mencionaron a <!subteam^{TEAM_ID}> en <#{channel}>\n"
                f"Link: {permalink}"
            )
        )
    next_turn()
