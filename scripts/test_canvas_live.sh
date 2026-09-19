#!/usr/bin/env bash
# Script para disparar el Webhook de Prueba de n8n (cuando pulsas el botón naranja en la UI)

MSG="${1:-hola}"
PHONE="${2:-5491155551234}"
NAME="${3:-Carlos Mendoza}"

echo "=================================================="
echo "Enviando evento de prueba al canvas de n8n..."
echo "URL: http://localhost:5678/webhook-test/whatsapp"
echo "Mensaje: '$MSG'"
echo "=================================================="

curl -i -X POST http://localhost:5678/webhook-test/whatsapp \
  -H "Content-Type: application/json" \
  -d "{
    \"object\": \"whatsapp_business_account\",
    \"entry\": [{
      \"id\": \"TEST_WHATSAPP_ID\",
      \"changes\": [{
        \"value\": {
          \"messaging_product\": \"whatsapp\",
          \"contacts\": [{\"profile\": {\"name\": \"$NAME\"}, \"wa_id\": \"$PHONE\"}],
          \"messages\": [{
            \"from\": \"$PHONE\",
            \"id\": \"wamid.test.$(date +%s)\",
            \"timestamp\": \"$(date +%s)\",
            \"text\": {\"body\": \"$MSG\"},
            \"type\": \"text\"
          }]
        },
        \"field\": \"messages\"
      }]
    }]
  }"

echo -e "\n=================================================="
echo "¡Evento enviado! Revisa tu pantalla de n8n para ver los nodos iluminados."
echo "=================================================="
