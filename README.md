# 🏭 Inventory Management Bot v4.0

Sistema de gestión de inventarios profesional integrado con **Telegram**, **Google Sheets** y una **Telegram Mini App** moderna.

## 🚀 Características Principales

*   📥 **Gestión de Stock:** Entradas (`/in`) y Salidas (`/out`) en tiempo real.
*   🔎 **Búsqueda Avanzada:** Encuentra productos por SKU, nombre o descripción con `/buscar`.
*   🚨 **Vigilancia (Watchdog):** Alertas automáticas cada hora para productos con stock bajo o agotados (🔴 Critico / 🟠 Bajo).
*   📱 **Mini App:** Interfaz visual moderna integrada nativamente en Telegram (React + Vite).
*   📊 **Google Sheets:** Base de datos persistente y fácil de auditar.
*   📝 **Bitácora Automática:** Todas las interacciones se guardan en la pestaña `notes`.

## 🛠️ Comandos de Telegram

*   `/start` - Inicia el bot y activa el monitoreo automático.
*   `/in <sku> <cantidad>` - Registra una entrada de inventario.
*   `/out <sku> <cantidad>` - Registra una salida de inventario.
*   `/buscar <texto>` - Busca productos en el inventario.
*   `/check` - Reporte instantáneo de alertas de stock.

## ☁️ Guía de Despliegue (Siempre Online)

Este bot está listo para correr 24/7 en plataformas como **Railway.app**, **Render** o **Heroku**.

### Pasos para Nube:
1.  **Sube a GitHub:** (Ya realizado: `git push origin main`).
2.  **Conecta la Nube:** En Railway, crea un "Nuevo Proyecto" desde tu repo.
3.  **Variables de Entorno:** Configura estas variables en tu panel de control:
    *   `TELEGRAM_BOT_TOKEN`: Tu token de BotFather.
    *   `GOOGLE_SPREADSHEET_ID`: El ID de tu hoja de cálculo.
    *   `GOOGLE_CREDENTIALS_JSON`: El **contenido completo** de tu archivo JSON (puedes encontrarlo listo para copiar en el archivo `secret_for_cloud.txt` generado localmente).

## 🖥️ Mini App (Desarrollo Local)

Para ver la interfaz gráfica:
1.  `cd miniapps/inventory-dashboard`
2.  `npm install`
3.  `npm run dev`

---
Diseñado por Antigravity AI 🤖