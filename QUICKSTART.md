# 🚀 Guía de Inicio Rápido - Telegram Bot

## ⚡ Configuración en 5 Minutos

### ✅ Checklist de Pre-requisitos

Antes de empezar, asegúrate de tener:
- [ ] Python 3.9 o superior instalado
- [ ] Una cuenta de Telegram
- [ ] Una cuenta de Google

---

## 📱 Paso 1: Crear tu Bot de Telegram (2 minutos)

1. Abre Telegram en tu teléfono o computadora
2. Busca: `@BotFather`
3. Envía: `/newbot`
4. Sigue las instrucciones:
   - **Nombre del bot**: "Mi Bot de Mensajes" (puede ser cualquier nombre)
   - **Username del bot**: debe terminar en "bot" (ej: `mi_mensajes_bot`)
5. **Copia el token** que te da BotFather (algo como: `123456789:ABCdefGHI...`)

✅ **Guarda el token**, lo necesitarás en el Paso 4

---

## 🔐 Paso 2: Obtener Credenciales de Google (5 minutos)

### Opción A: Proceso Completo (Primera vez)

1. Ve a: https://console.cloud.google.com/
2. **Crear proyecto**:
   - Haz clic en el selector de proyecto (arriba)
   - "New Project" → Nombre: "telegram-bot"
3. **Habilitar API**:
   - Menú → "APIs & Services" → "Library"
   - Busca "Google Sheets API" → Habilitar
4. **Crear Service Account**:
   - "APIs & Services" → "Credentials"
   - "+ CREATE CREDENTIALS" → "Service Account"
   - Nombre: "telegram-bot" → CREATE
   - Rol: "Editor" → CONTINUE → DONE
5. **Generar clave JSON**:
   - Haz clic en el email de la service account creada
   - Pestaña "KEYS" → "ADD KEY" → "Create new key"
   - Tipo: JSON → CREATE
   - **Se descargará un archivo .json** ← ¡Guárdalo bien!

✅ **Descarga el archivo JSON** y guárdalo en la carpeta del proyecto

### Opción B: Link Rápido (Si ya tienes un proyecto)

Si ya tienes un proyecto de Google Cloud:
1. https://console.cloud.google.com/iam-admin/serviceaccounts
2. Selecciona tu proyecto → CREATE SERVICE ACCOUNT
3. Sigue los pasos 4-5 de arriba

---

## 📊 Paso 3: Crear Google Spreadsheet (1 minuto)

1. Ve a: https://sheets.google.com/
2. Crea una hoja nueva (botón +)
3. Nómbrala: "Telegram Messages"
4. **IMPORTANTE**: Haz clic en "Share" (Compartir)
5. Pega el email de tu service account:
   - Lo encuentras en el archivo JSON descargado
   - Campo: `client_email`
   - Ej: `telegram-bot@proyecto-123.iam.gserviceaccount.com`
6. Dale permisos de **Editor** → Send
7. **Copia el ID de la URL**:
   ```
   https://docs.google.com/spreadsheets/d/[COPIA_ESTE_ID]/edit
   ```

✅ **Guarda el ID de la hoja**, lo necesitarás en el Paso 4

---

## ⚙️ Paso 4: Configurar el Bot (2 minutos)

### A. Instalar dependencias

```powershell
cd C:\Users\FELIX\Desktop\fronted\telegram-bot-ai-orchestrator
pip install -r requirements.txt
```

### B. Configurar variables de entorno

```powershell
# Crea el archivo .env
cp .env.example .env
```

Ahora edita `.env` con tus valores:

```bash
# Pega el token de BotFather (Paso 1)
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# Pon la ruta a tu archivo JSON (Paso 2)
GOOGLE_SERVICE_ACCOUNT_JSON=./credentials.json

# Pega el ID de la hoja (Paso 3)
GOOGLE_SPREADSHEET_ID=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
```

### C. Mover el archivo de credenciales

```powershell
# Mueve el archivo JSON descargado a la carpeta del proyecto
# Renómbralo a "credentials.json"
Move-Item "C:\Users\FELIX\Downloads\tu-proyecto-123abc.json" ".\credentials.json"
```

---

## 🎉 Paso 5: ¡Ejecutar el Bot!

```powershell
python src/main.py
```

Deberías ver:
```
✓ Google Sheets integration initialized successfully
🤖 Bot started successfully! Press Ctrl+C to stop.
```

---

## 🧪 Paso 6: Probar el Bot

1. Abre Telegram
2. Busca tu bot por su username (ej: `@mi_mensajes_bot`)
3. Envía: `/start`
4. El bot responderá: "👋 Welcome! Send me any message and I'll save it to Google Sheets."
5. Envía cualquier mensaje (ej: "Hola mundo")
6. El bot confirmará: "✓ Message saved successfully!"
7. **Revisa tu Google Sheet** - ¡debería aparecer el mensaje!

---

## 📋 Estructura de Datos en Google Sheets

El bot guardará cada mensaje con:

| Timestamp | User ID | Username | Message | Status |
|-----------|---------|----------|---------|--------|
| 2025-12-21T09:00:00 | 123456789 | @usuario | Hola mundo | Message received |

---

## ❓ Solución de Problemas

### "TELEGRAM_BOT_TOKEN not set"
✅ Verifica que `.env` existe y tiene el token correcto

### "Failed to initialize Google Sheets"
✅ Verifica que:
- El archivo `credentials.json` existe en la carpeta del proyecto
- La ruta en `.env` es correcta
- La hoja está compartida con el email de la service account

### El bot no responde en Telegram
✅ Verifica que:
- El bot está ejecutándose (ves el mensaje "Bot started successfully")
- Usaste el username correcto del bot
- No hay errores en la consola

### "Permission denied" en Google Sheets
✅ Asegúrate de haber compartido la hoja con el `client_email` del JSON

---

## 🎯 Comandos Útiles

```powershell
# Ejecutar el bot
python src/main.py

# Instalar dependencias
pip install -r requirements.txt

# Codificar credenciales a Base64 (para producción)
python encode_credentials.py

# Ver estructura del proyecto
tree /F
```

---

## 📚 Documentación Adicional

- **Credenciales detalladas**: Ver `GOOGLE_CREDENTIALS_GUIDE.md`
- **Codificar a Base64**: Ejecutar `encode_credentials.py`
- **README completo**: Ver `README.md`

---

## 🎊 ¡Listo!

Si todo funcionó:
- ✅ Tu bot está corriendo
- ✅ Responde en Telegram
- ✅ Guarda mensajes en Google Sheets

**Siguiente paso**: Personaliza el bot según tus necesidades editando `src/main.py`

¿Problemas? Revisa los logs en la consola donde ejecutaste el bot.
