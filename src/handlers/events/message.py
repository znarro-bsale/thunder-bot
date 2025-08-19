import requests
from ...config import TEAM_ID, SOURCE_CHANNEL_IDS, DEST_CHANNEL_IDS, DISCORD_WEBHOOK_URL
from ...db import get_current, next_turn

_seen_event_ids = set()


def handle_message(body, event, client):
    try:
        event_id = body.get("event_id")
        if event_id in _seen_event_ids:
            return
        _seen_event_ids.add(event_id)

        print("Evento: ", event)
        channel = event.get("channel")
        if channel not in SOURCE_CHANNEL_IDS:
            print("No es channel de origen")
            return

        if event.get("bot_id"):
            print("Es un bot")
            return

        text = event.get("text", "") or ""
        mention_token = f"<!subteam^{TEAM_ID}>"
        if mention_token not in text:
            print("No nos mencionaron")
            return

        permalink = client.chat_getPermalink(channel=channel, message_ts=event.get("ts")).get("permalink")

        support_member = get_current()

        if not support_member:
            support_member = next_turn()

        if not support_member:
            # Notify Discord
            requests.post(DISCORD_WEBHOOK_URL, json={
                "username": "ThunderBot",
                "avatar_url": "https://static.wikia.nocookie.net/the-scrappy/images/b/bc/Screenshot_Snarf.jpg",
                "content": f"🔔 Hey, nos mencionaron en canal de soporte\n"
                f"Link: {permalink}"
            })

            # Notify Slack
            for dest_chan in DEST_CHANNEL_IDS:
                client.chat_postMessage(
                    channel=dest_chan,
                    text=(
                        f"🔔 Hey <!subteam^{TEAM_ID}>, nos mencionaron en <#{channel}> y no hay turno asignado\n"
                        f"Link: {permalink}"
                    ),
                    blocks=[
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": (
                                    f"🔔 Hey <!subteam^{TEAM_ID}>, nos mencionaron en <#{channel}> y no hay turno asignado\n"
                                    f"Link: {permalink}"
                                )
                            }
                        },
                        {
                            "type": "actions",
                            "elements": [
                                {
                                    "type": "button",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Deshacer (no era SOS)"
                                    },
                                    "style": "danger",
                                    "action_id": "undo_shift",
                                    "value": "undo_shift"
                                }
                            ]
                        }
                    ]
                )
            return

        print("SOS para: ", support_member['name'])

        # Notify Discord
        requests.post(DISCORD_WEBHOOK_URL, json={
            "username": "ThunderBot",
            "avatar_url": "https://static.wikia.nocookie.net/the-scrappy/images/b/bc/Screenshot_Snarf.jpg",
            "content": f"🔔 Hey <@{support_member['discord_user_id']}>, nos mencionaron en canal de soporte\n"
            f"Link: {permalink}"

        })

        # Notify Slack
        for dest_chan in DEST_CHANNEL_IDS:
            client.chat_postMessage(
                channel=dest_chan,
                text=(
                    f"🔔 Hey <@{support_member['slack_user_id']}>, mencionaron al equipo en <#{channel}>\n"
                    f"Link: {permalink}"
                ),
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": (
                                f"🔔 Hey <@{support_member['slack_user_id']}>, mencionaron al equipo en <#{channel}>\n"
                                f"Link: {permalink}"
                            )
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Deshacer (no era SOS)"
                                },
                                "style": "danger",
                                "action_id": "undo_shift",
                                "value": "undo_shift"
                            }
                        ]
                    }
                ]
            )
        next_turn()
    except Exception as e:
        print("Error: ", e)
