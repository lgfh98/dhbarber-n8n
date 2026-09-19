# 💈 Orquestador WhatsApp + n8n + Spring Boot (Peluquería Daniel)

Proyecto de automatización conversacional que integra **WhatsApp Business (Meta Cloud API)** con un backend en **Spring Boot** utilizando **n8n** como motor de orquestación y **Redis** como gestor de estado y contexto.

---

## 🚀 Inicio Rápido

### 1. Iniciar los Servicios
```bash
# 1. Levantar n8n y Redis en segundo plano
docker compose up -d

# 2. Levantar el Backend Spring Boot (en otra terminal)
cd dhbarber-mvp && ./gradlew bootRun
```

### 2. Probar el Bot de WhatsApp

#### Opción A: Conversación Completa Interactiva (Simulador)
```bash
./scripts/simulate_whatsapp_chat.py
```
> Escribe `hola`, elige barbero (`1`, `2` o `3`), servicio y fecha (`2026-11-20 16:00`).

#### Opción B: Prueba Visual en el Canvas de n8n
1. Abre [http://localhost:5678/workflow/WfBarberAssist01](http://localhost:5678/workflow/WfBarberAssist01).
2. Haz clic en el botón naranja **"Execute workflow"**.
3. En tu terminal ejecuta:
   ```bash
   ./scripts/test_canvas_live.sh
   ```
4. Observa cómo todos los nodos se iluminan en verde en tiempo real.

---

## 📚 Documentación Completa

Para revisar la arquitectura detallada, diagramas Mermaid, explicación nodo a nodo de n8n, manejo de errores RFC 9457 y guía de despliegue con Meta Cloud API:

👉 **[Consulta la Documentación del Sistema](docs/DOCUMENTACION_SISTEMA.md)**
