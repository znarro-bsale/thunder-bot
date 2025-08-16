from slack_bolt import App
from .config import BOT_TOKEN
from .handlers.events.message import handle_message
from .handlers.commands.shift_status import handle_shift_status_command
from .handlers.commands.shift_next import handle_shift_next_command
from .handlers.commands.shift_prev import handle_shift_prev_command
from .handlers.commands.shift_active import handle_shift_active_command
from .handlers.commands.help import handle_help_command


def create_app():
    app = App(token=BOT_TOKEN)

    # Eventos
    app.event("message")(handle_message)

    # Comandos
    app.command("/shift-status")(handle_shift_status_command)
    app.command("/shift-next")(handle_shift_next_command)
    app.command("/shift-prev")(handle_shift_prev_command)
    app.command("/shift-active")(handle_shift_active_command)
    app.command("/help")(handle_help_command)

    return app
