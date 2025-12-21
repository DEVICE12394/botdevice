# Telegram Bot Simple

Bot de Telegram que guarda mensajes localmente (sin necesidad de Google Sheets).

## 🚀 Inicio Rápido

### 1. Obtén tu Token de Telegram (2 minutos)

1. Abre Telegram
2. Busca: `@BotFather`
3. Envía: `/newbot`
4. Sigue las instrucciones
5. **Copia el token**

### 2. Configura el Bot

Edita el archivo `.env` y pega tu token:

```bash
TELEGRAM_BOT_TOKEN=tu_token_aqui
```

### 3. Ejecuta el Bot

```bash
python src/main.py
```

¡Listo! 🎉

## 📝 Características

- ✅ Bot de Telegram funcional
- ✅ Guarda mensajes en archivo local (`logs/messages.log`)
- ✅ Comando `/start` - Mensaje de bienvenida
- ✅ Comando `/stats` - Estadísticas de mensajes
- ✅ No requiere configuración de Google Sheets
- ✅ Fácil de configurar (solo necesitas el token)

## 🎯 Uso

Una vez que el bot esté corriendo:

1. Busca tu bot en Telegram por su username
2. Envía `/start`
3. Envía cualquier mensaje
4. El bot lo guardará en `logs/messages.log`
5. Usa `/stats` para ver estadísticas

## 📊 Archivos Generados

- `logs/messages.log` - Todos los mensajes guardados
- Formato: `FECHA | USER_ID | USERNAME | MENSAJE`

## 🔧 Requisitos

```bash
pip install -r requirements.txt
```

## ❓ Solución de Problemas

### "TELEGRAM_BOT_TOKEN not set"
→ Asegúrate de que el archivo `.env` existe y contiene tu token

### El bot no responde
→ Verifica que el token sea correcto
→ Asegúrate de que el bot esté corriendo

## 🎨 Personalización

Edita `src/main.py` para:
- Cambiar mensajes de bienvenida
- Agregar nuevos comandos
- Modificar el formato del log
- Agregar más funcionalidades

---

**¿Quieres agregar Google Sheets después?**
Ver: `GOOGLE_VISUAL_GUIDE.html` para instrucciones completas.