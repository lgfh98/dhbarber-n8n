#!/usr/bin/env python3
"""
Simulador Interactivo de WhatsApp Meta Cloud API para n8n
Permite interactuar con el Webhook de n8n simulando mensajes de WhatsApp.
"""

import sys
import json
import time
import urllib.request
import urllib.error

N8N_WEBHOOK_URL = "http://localhost:5678/webhook/whatsapp"
N8N_TEST_WEBHOOK_URL = "http://localhost:5678/webhook-test/whatsapp"

CUSTOMER_PHONE = "5491155551234"
CUSTOMER_NAME = "Carlos Mendoza"

def build_meta_payload(message_text, phone=CUSTOMER_PHONE, name=CUSTOMER_NAME):
    return {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "META_WHATSAPP_ACCOUNT_ID",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "+5491155550000",
                                "phone_number_id": "PHONE_NUMBER_ID"
                            },
                            "contacts": [
                                {
                                    "profile": {
                                        "name": name
                                    },
                                    "wa_id": phone
                                }
                            ],
                            "messages": [
                                {
                                    "from": phone,
                                    "id": f"wamid.{int(time.time() * 1000)}",
                                    "timestamp": str(int(time.time())),
                                    "text": {
                                        "body": message_text
                                    },
                                    "type": "text"
                                }
                            ]
                        },
                        "field": "messages"
                    }
                ]
            }
        ]
    }

def send_message(text, url=N8N_WEBHOOK_URL):
    payload = build_meta_payload(text)
    data = json.dumps(payload).encode("utf-8")
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            body = response.read().decode("utf-8")
            return status, body
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")
    except urllib.error.URLError as e:
        return None, str(e.reason)

def main():
    print("=======================================================")
    print("  SIMULADOR DE CLIENTE DE WHATSAPP (Meta Cloud API)")
    print("  Conectado a n8n:", N8N_WEBHOOK_URL)
    print("  Cliente:", CUSTOMER_NAME, f"({CUSTOMER_PHONE})")
    print("=======================================================")
    print("Instrucciones:")
    print(" - Escribe 'hola' para iniciar la conversación.")
    print(" - Escribe 'salir' o presiona Ctrl+C para terminar.")
    print("-------------------------------------------------------\n")

    url = N8N_WEBHOOK_URL
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        url = N8N_TEST_WEBHOOK_URL
        print(f"Modo TEST activado -> {url}\n")

    while True:
        try:
            user_input = input(f"[{CUSTOMER_NAME} 📱] > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("salir", "exit", "quit"):
                print("Simulación finalizada.")
                break

            status, body = send_message(user_input, url)
            if status is None:
                print(f"⚠️ Error al conectar con n8n ({url}): {body}")
                print("Asegúrate de que n8n esté corriendo en el puerto 5678 y el workflow esté activo.\n")
            elif status in (200, 201):
                try:
                    res_json = json.loads(body)
                    if "responseText" in res_json:
                        print(f"\n[Bot Peluquería 💈]:\n{res_json['responseText']}\n")
                    else:
                        print(f"✅ Evento entregado a n8n: {body}\n")
                except Exception:
                    print(f"✅ Evento entregado a n8n: {body}\n")
            else:
                print(f"⚠️ n8n respondió con HTTP {status}: {body}\n")

        except KeyboardInterrupt:
            print("\nSimulación finalizada.")
            break

if __name__ == "__main__":
    main()
