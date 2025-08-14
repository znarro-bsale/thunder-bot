from slack_bolt import App
from .config import BOT_TOKEN
from .handlers.events.message import handle_message, handle_app_mention

def create_app():
    app = App(token=BOT_TOKEN)
    
    app.event("message")(handle_message)
    app.event("app_mention")(handle_app_mention)
    
    return app
