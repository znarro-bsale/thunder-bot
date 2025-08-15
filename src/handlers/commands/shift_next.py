from slack_bolt import Ack, Say
from ...db import advance_turn

def handle_shift_next_command(ack: Ack, say: Say, body: dict):
    ack()

    user_id = body["user_id"]

    next_member = advance_turn()

    if next_member:
        say(f"<@{user_id}>, pasaste el turno. Le toca a _*{next_member['name']}*_")
    else:
        say(f"<@{user_id}>, no se pudo pasar el turno. No hay miembros activos")
