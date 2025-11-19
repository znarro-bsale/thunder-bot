# Thunder Bot
Slack bot para el manejo de turnos de soporte dentro de ThunderTeam

## Instalación
1. Clonar el repositorio
2. Crear un archivo `.env` en la raíz del proyecto con las variables de entorno necesarias
3. Ejecutar `docker compose up -d` para iniciar el contenedor

## Variables de entorno
- `SLACK_BOT_TOKEN`: Token de Slack para el bot
- `SLACK_APP_TOKEN`: Token de Slack para la aplicación
- `TEAM_ID`: ID del equipo de Slack
- `SOURCE_CHANNEL_IDS`: IDs de los canales de Slack de origen (donde el bot escucha los mensajes)
- `DEST_CHANNEL_IDS`: IDs de los canales de Slack de destino (donde el bot envía los mensajes)
- `ALLOWED_COMMAND_CHANNEL`: ID del canal de Slack donde se permiten los comandos
- `DISCORD_WEBHOOK_URL`: URL del webhook de Discord
- `TURSO_DATABASE_URL`: URL de la base de datos Turso
- `TURSO_AUTH_TOKEN`: Token de autenticación de Turso

## Comandos
- `/shift-status` — Ver turnos (actual destacado)
- `/shift-pass` — Pasar turno al siguiente
- `/shift-undo` — Revierte última asignación
- `/shift-active @usuario on|off` — Activar/pausar miembro
- `/shift-country PE|CL on|off` — Activar/pausar por país
- `/help` — Muestra este mensaje
