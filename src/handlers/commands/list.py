from slack_bolt import Ack, Say
from ...db import get_members

def handle_list_command(ack: Ack, say: Say):
    ack()

    members = get_members()
    if members:
        message = "Lista de miembros:\n"
        for member in members:
            message += f"{member['id']}. {member['name']}\n"
        say(message)
    else:
        say("No hay miembros en la lista")
