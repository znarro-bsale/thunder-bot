from slack_bolt import Ack, Respond


def handle_help_command(ack: Ack, respond: Respond):
    """Ayuda para los comandos disponibles"""
    ack()

    HELP = (
        "*Comandos disponibles:*\n"
        "`/shift-status` — Ver turnos (actual destacado)\n"
        "`/shift-next` — Pasar turno al siguiente\n"
        "`/shift-prev` — Pasar turno al anterior\n"
        "`/shift-undo` — Revierte última asignación\n"
        "`/shift-assign @usuario` — Asignar turno manualmente\n"
        "`/shift-active set @usuario on|off` — Activar/pausar miembro\n"
        "`/shift-country PE|CL on|off` — Activar/pausar por país\n"
        "`/help` — Muestra este mensaje\n"
    )

    respond(HELP)
