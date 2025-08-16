from slack_bolt import Ack, Say
from ...db import previous_turn


def handle_undo_shift_button(ack: Ack, say: Say, body: dict, client):
    """Maneja el botón de deshacer turno cuando no era una alerta real"""
    ack()
    
    user_id = body['user']['id']
    channel_id = body['channel']['id']
    message_ts = body['message']['ts']
    
    # Ejecutar la lógica de deshacer turno
    prev_member = previous_turn()
    
    if not prev_member:
        say(f"⚠️ <@{user_id}>, no se pudo restaurar el turno anterior. No hay miembros activos")
        return

    # Obtener los bloques originales del mensaje
    original_blocks = body['message']['blocks']
    
    # Modificar el botón para mostrar que ya fue usado
    updated_blocks = []
    for block in original_blocks:
        if block['type'] == 'actions':
            # Reemplazar el botón con uno deshabilitado
            updated_block = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"✅ _Deshecho por <@{user_id}>_. Volvió el turno a _*{prev_member['name']}*_"
                }
            }
            updated_blocks.append(updated_block)
        else:
            updated_blocks.append(block)

    # Actualizar el mensaje para deshabilitar el botón
    client.chat_update(
        channel=channel_id,
        ts=message_ts,
        blocks=updated_blocks
    )

        