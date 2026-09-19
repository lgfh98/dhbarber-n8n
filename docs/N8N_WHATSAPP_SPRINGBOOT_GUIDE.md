# Guía Didáctica: Integración de WhatsApp (Meta Cloud API) + n8n + Backend Spring Boot

Esta guía explica paso a paso cómo funciona la arquitectura de automatización para **Peluquería Daniel**, conectando la experiencia conversacional de WhatsApp con tu API existente de Spring Boot.

---

## 1. La Arquitectura en 4 Capas

```
[ Capa de Usuario ]         Cliente escribe por WhatsApp
         ↕
[ Capa Oficial Meta ]      Meta WhatsApp Cloud API (Graph API)
         ↕ (Webhooks HTTP)
[ Orquestador n8n ]        n8n (Lógica de conversación + Gestión de sesión)
  ├── 1. Webhook Inbound    Recibe los mensajes de WhatsApp
  ├── 2. Redis Session      Recuerda en qué paso está el cliente
  ├── 3. Router Conversacional Valida opciones (Barbero -> Servicio -> Fecha)
  ├── 4. HTTP Request Node  Llama a tu backend Spring Boot (Puerto 8080)
  └── 5. Outbound Node      Envía la respuesta a WhatsApp
         ↕ (REST JSON)
[ Core Backend ]           Tu API de Spring Boot (H2 / Base de Datos)
```

---

## 2. Conceptos Fundamentales de n8n para Principiantes

Si n8n es nuevo para ti, piensa en él como un **árbol de bloques visuales** donde cada bloque (nodo) recibe datos en formato JSON, realiza una acción y pasa el resultado al siguiente nodo:

1. **Trigger Node (Disparador):** El nodo que inicia el flujo. En nuestro caso, el nodo `Webhook`. Se queda escuchando peticiones HTTP en una URL específica (ej. `/webhook/whatsapp`).
2. **Action Nodes (Nodos de Acción):**
   - **HTTP Request:** Funciona como un Postman automatizado. Hace peticiones `GET`, `POST`, `PUT` a tu API Spring Boot.
   - **Redis:** Guarda y lee datos clave-valor ultra rápidos en memoria.
3. **Flow Control & Logic (Lógica y Código):**
   - **Code Node:** Te permite escribir código JavaScript moderno para transformar datos, formatear textos o validar entradas.
   - **Switch Node:** Funciona como un `switch/case` o `if/else`, desviando el flujo según el estado de la conversación.

---

## 3. ¿Por qué necesitamos Gestión de Estado (Session) en WhatsApp?

A diferencia de un formulario web donde el usuario llena todo y hace clic en "Enviar", en WhatsApp la interacción es **mensaje por mensaje**:

1. Cliente: *"Hola"*
2. Bot: *"¿Con qué barbero te quieres atender? (1. Daniel, 2. Mateo, 3. Valentina)"*
3. Cliente: *"Mateo"*
4. Bot: *"¿Qué servicio deseas? (1. Corte Fade, 2. Barba, 3. Combo)"*
5. Cliente: *"1"*
6. Bot: *"¿Para qué día y hora? (ej: 2026-11-20 16:00)"*
7. Cliente: *"2026-11-20 16:00"*

Cada mensaje llega como una petición HTTP independiente sin memoria. Para saber qué significa *"1"* en el paso 5, **Redis** guarda el contexto asociado al número de teléfono del usuario (`session:5491155551234`):

```json
{
  "state": "WAITING_SERVICE",
  "barberId": "barber-mateo",
  "barberName": "Mateo Silva",
  "customerId": "carlos-mendoza",
  "customerPhone": "+5491155551234"
}
```

Cuando el cliente finalmente envía la fecha y hora, n8n junta todos los datos recolectados y arma el JSON que exige tu backend Spring Boot:

```json
POST http://host.docker.internal:8080/api/appointments
{
  "barberId": "barber-mateo",
  "customerId": "carlos-mendoza",
  "customerPhone": "+5491155551234",
  "serviceIds": ["corte-fade"],
  "startTime": "2026-11-20T16:00:00",
  "durationMinutes": 45
}
```

---

## 4. Manejo de Respuestas y Errores de Negocio (RFC 9457)

Tu API en Spring Boot implementa el estándar moderno de errores **RFC 9457 ProblemDetail**:
- Si el turno está disponible: Spring Boot responde **HTTP 201 Created** y n8n envía:
  > *"🎉 ¡Turno confirmado con éxito! Barbero: Mateo Silva | Fecha: 2026-11-20 16:00 hs"*
- Si el barbero ya está ocupado a esa hora: Spring Boot responde **HTTP 422 Unprocessable Entity** con:
  ```json
  {
    "status": 422,
    "title": "Domain Invariant Violation",
    "detail": "El barbero barber-mateo ya cuenta con una cita en el rango horario solicitado"
  }
  ```
  n8n captura ese `detail` y le responde al cliente en WhatsApp:
  > *"⚠️ No fue posible agendar tu turno: El barbero ya cuenta con una cita en el rango horario solicitado. Por favor elige otro horario."*

---

## 5. Pruebas Locales con el Simulador

Hemos creado un simulador en Python (`scripts/simulate_whatsapp_chat.py`) que emula exactamente las cargas de Meta Cloud API:

```bash
# Ejecutar el simulador interactivo en terminal
./scripts/simulate_whatsapp_chat.py
```

Podrás escribir:
1. `hola` -> n8n consultará tu Spring Boot `GET /api/barbers` y te mostrará el catálogo.
2. `2` -> Selecciona a Mateo Silva.
3. `1` -> Selecciona Corte Fade (45 min).
4. `2026-11-20 16:00` -> Envía la reserva a Spring Boot y confirma la cita en la base de datos.

---

## 6. Conexión Real con Meta Cloud API (WhatsApp Business)

Cuando quieras conectar el número real de WhatsApp de la peluquería:

1. **Crear App en Meta Developers:**
   - Ve a [developers.facebook.com](https://developers.facebook.com).
   - Crea una app tipo **Business** y agrega el producto **WhatsApp**.
2. **Obtener Credenciales:**
   - **Phone Number ID:** Identificador numérico del número asignado para pruebas.
   - **User Access Token:** Token Bearer con permisos `whatsapp_business_messaging`.
3. **Configurar el Webhook:**
   - Usa un túnel (como **Cloudflare Tunnel** o **Ngrok**):
     ```bash
     ngrok http 5678
     ```
   - En el panel de Meta, en **Configuration > Webhook**, pega:
     `https://tu-subdominio.ngrok-free.app/webhook/whatsapp`
   - En **Verify Token**, escribe tu token secreto (ej. `dhbarber_secret_token_123`).
   - Suscríbete al evento `messages`.
