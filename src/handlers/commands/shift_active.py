from slack_bolt import Ack, Say
from ...db import get_member_by_slack_id, next_turn, set_member_state
from ...utils.channel_validator import validate_channel


def handle_shift_active(ack: Ack, say: Say, body: dict):
    """Activa o desactiva un miembro (no entra en la rotación)"""
    if not validate_channel(ack, body):
        return

    ack()

    text = body.get('text', '').strip()
    if not text:
        say("Formato incorrecto. Uso: `/shift-active @usuario on|off`")
        return

    parts = text.split()
    if len(parts) != 2:
        say("Formato incorrecto. Uso: `/shift-active @usuario on|off`")
        return

    member, state = parts

    if not member.startswith('<@') or not member.endswith('>'):
        say("Debes mencionar un usuario válido. Ejemplo: `@usuario`")
        return

    try:
        slack_user_id = member.split('|')[0][2:]
        if not slack_user_id:
            raise ValueError("Invalid member ID")

        member = get_member_by_slack_id(slack_user_id)
        if not member:
            say("Usuario no encontrado")
            return
    except (IndexError, ValueError):
        say("Formato de usuario inválido")
        return

    if state.lower() not in ['on', 'off']:
        say("Estado inválido. Usa `on` para activar o `off` para desactivar")
        return

    user_id = body['user_id']
    new_state = 1 if state.lower() == 'on' else 0

    # TODO: esto debe ir en transaction
    if new_state == 0 and member['is_current'] == 1:
        next_turn()
    result = set_member_state(member['id'], new_state)
    if result:
        state_text = "activo" if new_state == 1 else "inactivo"
        say(f"✅ <@{user_id}>, se cambió el estado de <@{slack_user_id}> a {state_text}")
    else:
        say(f"⚠️ <@{user_id}>, no se pudo cambiar el estado de <@{slack_user_id}>")
