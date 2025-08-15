from slack_bolt import Ack, Say
from ...db import get_current

def handle_current_command(ack: Ack, say: Say):
    ack()

    current_member = get_current()
    if current_member:
        say(f"Es turno de {current_member['name']}")
    else:
        say("Nadie tiene turno en sqlite")
