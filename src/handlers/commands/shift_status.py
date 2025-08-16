from slack_bolt import Ack, Respond
from ...db import get_members
from ...utils.channel_validator import validate_channel


def handle_shift_status(ack: Ack, respond: Respond, body: dict):
    """Muestra el estado de los turnos"""
    if not validate_channel(ack, body):
        return

    ack()

    members = get_members()
    if members:
        message = "🔄 *Turnos:*\n"
        for member in members:
            message += "_*" if member['is_current'] else ""
            message += f"{member['id']}. {member['name']}"
            message += "*_" if member['is_current'] else ""
            message += "\n"
        respond(message)
    else:
        respond("No hay miembros activos en lista")
