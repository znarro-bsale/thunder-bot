from slack_bolt.adapter.socket_mode import SocketModeHandler
from src.bot import create_app
from src.config import APP_TOKEN

def main():
    app = create_app()
    handler = SocketModeHandler(app, APP_TOKEN)
    print("🚀 Thunder Bot iniciando...")
    handler.start()

if __name__ == "__main__":
    main()
