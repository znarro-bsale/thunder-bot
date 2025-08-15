from slack_bolt import Ack, Say
from ...db import next_turn


def handle_shift_next_command(ack: Ack, say: Say, body: dict):
    """Pasa el turno al siguiente miembro activo"""
    ack()

    user_id = body["user_id"]

    next_member = next_turn()

    if next_member:
        say(f"<@{user_id}>, pasaste el turno. Le toca a _*{next_member['name']}*_")
    else:
        say(f"<@{user_id}>, no se pudo pasar el turno. No hay miembros activos")
