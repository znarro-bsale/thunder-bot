from slack_bolt import Ack, Respond

def handle_shift_country_command(ack: Ack, respond: Respond):
    ack()
    respond("En desarrollo...")
    pass
