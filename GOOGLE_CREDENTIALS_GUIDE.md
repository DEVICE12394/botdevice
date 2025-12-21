# 📝 Guía: Cómo Obtener Credenciales de Google Service Account

## 🎯 Pasos para Obtener las Credenciales

### 1️⃣ Acceder a Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Inicia sesión con tu cuenta de Google

### 2️⃣ Crear o Seleccionar un Proyecto

1. En la parte superior, haz clic en el selector de proyecto
2. Haz clic en **"New Project"** (Nuevo Proyecto)
3. Nombra tu proyecto (ej: "telegram-bot-sheets")
4. Haz clic en **"Create"**

### 3️⃣ Habilitar Google Sheets API

1. Ve a **APIs & Services** > **Library**
2. Busca **"Google Sheets API"**
3. Haz clic en el resultado
4. Haz clic en el botón **"ENABLE"** (Habilitar)

### 4️⃣ Crear Service Account (Cuenta de Servicio)

1. Ve a **APIs & Services** > **Credentials**
2. Haz clic en **"+ CREATE CREDENTIALS"**
3. Selecciona **"Service Account"**
4. Completa los datos:
   - **Service account name**: `telegram-bot` (o el nombre que prefieras)
   - **Service account ID**: se generará automáticamente
   - **Description**: "Bot de Telegram para guardar mensajes"
5. Haz clic en **"CREATE AND CONTINUE"**
6. En **"Grant this service account access to project"**: 
   - Selecciona el rol **"Editor"** (opcional, pero facilita el acceso)
   - Haz clic en **"CONTINUE"**
7. Haz clic en **"DONE"**

### 5️⃣ Generar la Clave JSON

1. En la lista de Service Accounts, encuentra el que acabas de crear
2. Haz clic en el email de la service account
3. Ve a la pestaña **"KEYS"**
4. Haz clic en **"ADD KEY"** > **"Create new key"**
5. Selecciona formato **JSON**
6. Haz clic en **"CREATE"**
7. 🎉 **Se descargará automáticamente un archivo .json**

### 6️⃣ Crear Google Spreadsheet

1. Ve a [Google Sheets](https://sheets.google.com/)
2. Crea una nueva hoja de cálculo (Spreadsheet)
3. Nómbrala: "Telegram Bot Messages" (o como prefieras)
4. **IMPORTANTE**: Haz clic en **"Share"** (Compartir)
5. Copia el email de la service account (ej: `telegram-bot@project-id.iam.gserviceaccount.com`)
6. Pégalo en el campo de compartir y dale permisos de **Editor**
7. Copia el **ID de la hoja** de la URL:
   ```
   https://docs.google.com/spreadsheets/d/[ESTE_ES_EL_ID]/edit
   ```

### 7️⃣ Configurar las Variables de Entorno

Ahora tienes dos opciones para configurar `GOOGLE_SERVICE_ACCOUNT_JSON`:

#### Opción A: Usar la ruta al archivo (Más simple)

```bash
TELEGRAM_BOT_TOKEN=tu_token_de_telegram
GOOGLE_SERVICE_ACCOUNT_JSON=C:/Users/FELIX/Desktop/fronted/telegram-bot-ai-orchestrator/credentials.json
GOOGLE_SPREADSHEET_ID=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
```

1. Mueve el archivo `.json` descargado a la carpeta del proyecto
2. Renómbralo a `credentials.json`
3. Usa la ruta completa en `.env`

#### Opción B: Codificar en Base64 (Para producción/Docker)

Usa el script `encode_credentials.py` (ver abajo) para convertir el JSON a Base64:

```bash
python encode_credentials.py
```

Luego copia el resultado en tu `.env`:

```bash
GOOGLE_SERVICE_ACCOUNT_JSON=eyJ0eXBlIjoic2VydmljZV9hY2NvdW50IiwicHJvamVjdF9pZCI6InRlbGVncmFtLWJvdC1zaGVldHMi...
```

---

## 📋 Estructura del Archivo JSON

Tu archivo de credenciales descargado tendrá esta estructura:

```json
{
  "type": "service_account",
  "project_id": "telegram-bot-sheets",
  "private_key_id": "abc123def456...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "telegram-bot@telegram-bot-sheets.iam.gserviceaccount.com",
  "client_id": "123456789012345678901",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/...",
  "universe_domain": "googleapis.com"
}
```

---

## 🔒 Seguridad

⚠️ **IMPORTANTE**:
- ❌ **NUNCA** subas el archivo JSON a Git/GitHub
- ❌ **NUNCA** compartas las credenciales públicamente
- ✅ El archivo ya está incluido en `.gitignore`
- ✅ Para producción, usa Base64 o variables de entorno seguras
- ✅ Para desarrollo local, usa la ruta al archivo

---

## 🎯 Resumen Rápido

| Paso | Qué necesitas obtener | Dónde va |
|------|----------------------|----------|
| BotFather | Token del bot | `TELEGRAM_BOT_TOKEN` |
| Google Cloud | Archivo JSON de credenciales | `GOOGLE_SERVICE_ACCOUNT_JSON` |
| Google Sheets URL | ID de la hoja (parte de la URL) | `GOOGLE_SPREADSHEET_ID` |

---

## ❓ Problemas Comunes

### "Failed to initialize Google Sheets"

**Causa**: Credenciales inválidas o mal formateadas

**Solución**:
1. Verifica que el archivo JSON sea válido
2. Si usas Base64, asegúrate de que esté bien codificado
3. Verifica que no haya espacios o saltos de línea extra

### "Permission denied" al escribir en Sheets

**Causa**: La hoja no está compartida con la service account

**Solución**:
1. Abre tu Google Sheet
2. Haz clic en "Share"
3. Agrega el email de la service account (de client_email en el JSON)
4. Dale permisos de "Editor"

### "Spreadsheet not found"

**Causa**: ID incorrecto de la hoja

**Solución**:
1. Verifica el ID en la URL de tu Google Sheet
2. Asegúrate de copiar solo el ID, no toda la URL

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs del bot al iniciar
2. Verifica que todas las variables estén configuradas
3. Prueba primero con la opción A (ruta al archivo)
