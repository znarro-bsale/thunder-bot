from slack_bolt import Ack, Say
from ...db import previous_turn


def handle_shift_prev_command(ack: Ack, say: Say, body: dict):
    """Pasa el turno al miembro anterior activo"""
    ack()

    user_id = body["user_id"]

    prev_member = previous_turn()

    if prev_member:
        say(f"<@{user_id}>, pasaste el turno. Le toca a _*{prev_member['name']}*_")
    else:
        say(f"<@{user_id}>, no se pudo pasar el turno. No hay miembros activos")
