from slack_bolt import Ack, Respond
from ...utils.channel_validator import validate_channel


def handle_help(ack: Ack, respond: Respond, body: dict):
    """Ayuda para los comandos disponibles"""
    if not validate_channel(ack, body):
        return

    ack()

    HELP = (
        "💡 *Comandos disponibles:*\n"
        "`/shift-status` — Ver turnos (actual destacado)\n"
        "`/shift-pass` — Pasar turno al siguiente\n"
        "`/shift-undo` — Revierte última asignación\n"
        "`/shift-active @usuario on|off` — Activar/pausar miembro\n"
        "`/shift-country PE|CL on|off` — Activar/pausar por país\n"
        "`/help` — Muestra este mensaje\n"
    )

    respond(HELP)
