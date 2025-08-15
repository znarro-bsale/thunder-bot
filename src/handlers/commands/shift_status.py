from slack_bolt import Ack, Respond
from ...db import get_members


def handle_shift_status_command(ack: Ack, respond: Respond):
    """Muestra el estado de los turnos"""
    ack()

    members = get_members()
    if members:
        message = "*Turnos:*\n"
        for member in members:
            message += "_*" if member['is_current'] else ""
            message += f"{member['id']}. {member['name']}"
            message += "*_" if member['is_current'] else ""
            message += "\n"
        respond(message)
    else:
        respond("No hay miembros activos en lista")
