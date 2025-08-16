from slack_bolt import Ack, Respond
from ...utils.channel_validator import validate_channel


def handle_shift_country(ack: Ack, respond: Respond, body: dict):
    if not validate_channel(ack, body):
        return

    ack()
    respond("En desarrollo...")
    pass
