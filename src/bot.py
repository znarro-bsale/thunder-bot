from slack_bolt import App
from .config import BOT_TOKEN
# from .handlers.events.app_mention import handle_app_mention
from .handlers.events.message import handle_message
from .handlers.commands.shift_status import handle_shift_status_command
from .handlers.commands.shift_next import handle_shift_next_command
from .handlers.commands.help import handle_help_command

def create_app():
    app = App(token=BOT_TOKEN)
    # este puede brindar info de sus comandos?
    # app.event("app_mention")(handle_app_mention)
    app.event("message")(handle_message)
    app.command("/shift-status")(handle_shift_status_command)
    app.command("/shift-next")(handle_shift_next_command)
    app.command("/help")(handle_help_command)

    return app
