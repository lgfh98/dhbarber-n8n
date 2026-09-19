# 📋 TODO List: Automatización WhatsApp + n8n + Spring Boot

Este documento detalla el estado actual del proyecto y la hoja de ruta priorizada con las tareas pendientes para llevar el sistema desde el MVP actual hasta una solución lista para producción.

---

## 📊 Resumen de Estado

- **Completado:** 60% (Core, Arquitectura, Backend Spring Boot, Redis, Workflow n8n de Agendamiento, Simulador CLI y Pruebas en Vivo).
- **Pendiente:** 40% (Flujos adicionales de cancelación/consulta, conexión real a Meta Cloud API, dockerización total y recordatorios programados).

---

## ✅ Lo que ya está completado (Estado Actual)

- [x] **Backend Spring Boot:** Clonado, compilado y testeado en local (`dhbarber-mvp` en `:8080`).
- [x] **Endpoints Verificados:** `GET /api/barbers`, `GET /api/appointments/business-hours`, `POST /api/appointments`.
- [x] **Manejo de Invariantes de Negocio:** Captura y formateo de errores RFC 9457 `ProblemDetail` (HTTP 422).
- [x] **Entorno de Contenedores:** Docker Compose con **Redis 7** (sesiones) y **n8n 2.39** en `:5678`.
- [x] **Red Docker Interna:** Comunicación fluida `host.docker.internal` (n8n ➔ Spring Boot) y `redis:6379`.
- [x] **Gestión de Contexto (Session Manager):** Persistencia en Redis de la máquina de estados con TTL de 30 min.
- [x] **Workflow Core de Agendamiento:**
  - Menú de bienvenida dinámico desde la base de datos.
  - Selección de barbero.
  - Selección de servicio (Corte, Barba, Combo).
  - Validación de fecha/hora.
  - Creación de cita y confirmación con ID de reserva.
- [x] **Herramientas de Testing:** Simulador CLI (`simulate_whatsapp_chat.py`) y disparador de canvas (`test_canvas_live.sh`).
- [x] **Documentación Técnica:** Arquitectura, diagramas y guía didáctica nodo a nodo.

---

## 📌 Tareas Pendientes Priorizadas

### 🟢 Fase 1: Flujos Conversacionales Adicionales en n8n *(Prioridad Alta)*
- [ ] **1.1. Flujo de "Consultar mis turnos agendados":**
  - Consumir `GET /api/appointments` filtrando por el teléfono del cliente (`customerPhone`).
  - Responder al cliente con la lista de sus próximas citas activas (ID, barbero, fecha/hora).
- [ ] **1.2. Flujo de Cancelación de Citas:**
  - Permitir al usuario seleccionar una de sus citas activas.
  - Solicitar motivo de cancelación.
  - Consumir `PATCH /api/appointments/{id}/cancel` con el payload `{ "reason": "..." }`.
  - Confirmar la liberación del turno.
- [ ] **1.3. Flujo de Reprogramación de Citas:**
  - Seleccionar cita activa y solicitar nueva fecha/hora.
  - Consumir `PUT /api/appointments/{id}/reschedule` validando las 2 horas de anticipación mínima del negocio.
- [ ] **1.4. Mensajes Interactivos Nativos de WhatsApp (Botones y Listas):**
  - Reemplazar las opciones de texto (`1`, `2`, `3`) por botones interactivos de WhatsApp (`interactive.type: button_reply`) y menús de lista (`list_reply`).

---

### 🟡 Fase 2: Conexión Oficial con Meta Cloud API *(Prioridad Alta)*
- [ ] **2.1. Handshake de Verificación de Webhook (Meta Verification Challenge):**
  - Agregar al Webhook de n8n el manejo de peticiones HTTP `GET` para responder a `hub.challenge` con el `hub.verify_token` acordado.
- [ ] **2.2. Exposición Pública Segura (Túnel HTTPS):**
  - Configurar **Cloudflare Tunnel** o **Ngrok** apuntando a `localhost:5678`.
- [ ] **2.3. Configuración en Meta for Developers:**
  - Registrar la URL del webhook en el panel de Meta (`https://mi-dominio.com/webhook/whatsapp`).
  - Suscribir el webhook al campo `messages`.
- [ ] **2.4. Credenciales de Envío en n8n:**
  - Obtener el `PHONE_NUMBER_ID` y un **Access Token Permanente** (creando un *System User* en Meta Business Manager).
  - Configurar las variables en n8n para que el nodo `Outbound Meta WhatsApp` despache los mensajes directamente a la Graph API de Meta.

---

### 🟠 Fase 3: Notificaciones Proactivas y Recordatorios *(Prioridad Media)*
- [ ] **3.1. Webhook de Eventos desde Spring Boot a n8n:**
  - Conectar el Outbox Pattern de Spring Boot (`AppointmentEventListener`) con un webhook en n8n para enviar la confirmación inmediata de reserva en segundo plano.
- [ ] **3.2. Recordatorios Automáticos Programados:**
  - Crear un workflow con nodo **Schedule Trigger (Cron)** en n8n que consulte diariamente las citas de las próximas 24 horas y envíe un WhatsApp de recordatorio al cliente.

---

## 🔵 Fase 4: Despliegue, Persistencia y Producción *(Prioridad Media / Baja)*
- [ ] **4.1. Migración de Base de Datos (H2 ➔ PostgreSQL):**
  - Agregar servicio `postgres:16-alpine` al `docker-compose.yml`.
  - Configurar Spring Boot para persistir en PostgreSQL en lugar de H2 en memoria.
- [ ] **4.2. Dockerizar el Backend Spring Boot:**
  - Crear `Dockerfile` multi-stage para `dhbarber-mvp`.
  - Integrar el backend dentro del `docker-compose.yml` para levantar todo el ecosistema con un solo `docker compose up -d`.
- [ ] **4.3. Gestión de Secretos y Variables de Entorno:**
  - Crear archivo `.env` para centralizar credenciales (tokens de Meta, claves de DB, contraseñas de Redis).
