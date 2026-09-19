#!/usr/bin/env bash
set -e

WORKFLOW_FILE="$(cd "$(dirname "$0")/.." && pwd)/n8n/workflows/dhbarber_whatsapp_workflow.json"

if [ ! -f "$WORKFLOW_FILE" ]; then
  echo "Error: No se encontró el archivo de workflow en $WORKFLOW_FILE"
  exit 1
fi

echo "Verificando que el contenedor dhbarber-n8n esté activo..."
if ! docker ps | grep -q "dhbarber-n8n"; then
  echo "El contenedor dhbarber-n8n no está corriendo aún."
  echo "Ejecuta: docker compose up -d n8n"
  exit 1
fi

echo "Copiando workflow al contenedor..."
docker cp "$WORKFLOW_FILE" dhbarber-n8n:/tmp/dhbarber_whatsapp_workflow.json

echo "Importando workflow en n8n..."
docker exec -u node dhbarber-n8n n8n import:workflow --input=/tmp/dhbarber_whatsapp_workflow.json

echo "Publicando y activando workflow..."
docker exec -u node dhbarber-n8n n8n publish:workflow --id=WfBarberAssist01

echo "¡Workflow importado y publicado con éxito en n8n!"
