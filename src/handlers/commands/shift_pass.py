from slack_bolt import Ack, Say
from ...db import next_turn
from ...utils.channel_validator import validate_channel


def handle_shift_pass(ack: Ack, say: Say, body: dict):
    """Pasa el turno al siguiente miembro activo"""
    if not validate_channel(ack, body):
        return

    ack()

    user_id = body["user_id"]

    next_member = next_turn()

    if next_member:
        say(f"✅ <@{user_id}>, se pasó el turno a _*{next_member['name']}*_")
    else:
        say(f"⚠️ <@{user_id}>, no se pudo pasar el turno. No hay miembros activos")
