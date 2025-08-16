from ..config import ALLOWED_COMMAND_CHANNEL

def is_allowed_channel(channel_id: str) -> bool:
    if not ALLOWED_COMMAND_CHANNEL:
        return True

    return channel_id == ALLOWED_COMMAND_CHANNEL

def validate_channel(ack, body: dict) -> bool:
    channel_id = body.get('channel_id', '')

    if not is_allowed_channel(channel_id):
        ack()
        return False

    return True
