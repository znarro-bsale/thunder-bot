from slack_bolt import App
from .config import BOT_TOKEN
from .handlers.events.message import handle_message
from .handlers.commands.shift_status import handle_shift_status
from .handlers.commands.shift_pass import handle_shift_pass
from .handlers.commands.shift_active import handle_shift_active
from .handlers.commands.shift_country import handle_shift_country
from .handlers.commands.shift_undo import handle_shift_undo
from .handlers.commands.help import handle_help
from .handlers.actions.button_actions import handle_undo_shift_button


def create_app():
    app = App(token=BOT_TOKEN)

    # Eventos
    app.event("message")(handle_message)

    # Comandos
    app.command("/shift-status")(handle_shift_status)
    app.command("/shift-pass")(handle_shift_pass)
    app.command("/shift-undo")(handle_shift_undo)
    app.command("/shift-active")(handle_shift_active)
    app.command("/shift-country")(handle_shift_country)
    app.command("/help")(handle_help)
    
    # Acciones de botones
    app.action("undo_shift")(handle_undo_shift_button)

    return app
