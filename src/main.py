"""
Telegram Bot v4.0 - Full Inventory Management Suite
Features: Transactions, Search, Auto-Alerts, Watchdog, Logging
"""
import os
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes
)
import logging
from config.settings import TELEGRAM_BOT_TOKEN, GOOGLE_SERVICE_ACCOUNT_JSON

# --- Dashboard URL (Localtunnel) ---
DASHBOARD_URL = "https://bot-inventario-pro-99.loca.lt"

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Config ---
LOGS_DIR = "logs"
LOCAL_CREDENTIALS_FILE = "snappy-topic-481406-p9-3673e43ccb98.json"
SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID') or "1qQgazyaUQfNcoLNAxU5a2x9utAQl8zNE5FYMUPxdyQU"
CHECK_INTERVAL_MIN = 60

if not os.path.exists(LOGS_DIR): os.makedirs(LOGS_DIR)
LOG_FILE = os.path.join(LOGS_DIR, "messages.log")

def safe_float(val):
    try: return float(val)
    except: return 0.0

# --- Google Sheets Service ---
class GoogleSheetsService:
    def __init__(self):
        self.client = None
        self.inventory_sheet = None
        self.logs_sheet = None
        self.connected = False
        
    def connect(self):
        try:
            scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
            creds = None
            
            # 1. Try Local File
            if os.path.exists(LOCAL_CREDENTIALS_FILE):
                print(f"[INFO] Loading from local file: {LOCAL_CREDENTIALS_FILE}")
                creds = Credentials.from_service_account_file(LOCAL_CREDENTIALS_FILE, scopes=scopes)
            
            # 2. Try Env Var (Cloud Deployment)
            elif os.environ.get("GOOGLE_CREDENTIALS_JSON"):
                print("[INFO] Loading from Environment Variable")
                import json
                # Load JSON from string stored in Env Var
                creds_dict = json.loads(os.environ.get("GOOGLE_CREDENTIALS_JSON"))
                creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
            
            # 3. Fallback to older env var logic
            elif GOOGLE_SERVICE_ACCOUNT_JSON and os.path.exists(GOOGLE_SERVICE_ACCOUNT_JSON):
                creds = Credentials.from_service_account_file(GOOGLE_SERVICE_ACCOUNT_JSON, scopes=scopes)
            
            if not creds: 
                print("[ERROR] No credentials found (File or Env Var).")
                return False

            self.client = gspread.authorize(creds)
            spreadsheet = self.client.open_by_key(SPREADSHEET_ID)
            
            try: 
                self.inventory_sheet = spreadsheet.worksheet("Inventory")
            except:
                self.inventory_sheet = spreadsheet.get_worksheet(0)
            
            try: self.logs_sheet = spreadsheet.worksheet("notes")
            except:
                try: 
                    self.logs_sheet = spreadsheet.add_worksheet("notes", 1000, 10)
                    self.logs_sheet.append_row(["Timestamp", "User", "Action", "Context"])
                except: self.logs_sheet = self.inventory_sheet

            self.connected = True
            print(f"[OK] Connected: {spreadsheet.title}")
            return True
        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")
            return False

    def append_log(self, data):
        if not self.connected and not self.connect(): return False
        try: self.logs_sheet.append_row(data); return True
        except: 
             if self.connect():
                 try: self.logs_sheet.append_row(data); return True
                 except: pass
             return False

    def update_stock(self, sku, delta):
        """Transactional update"""
        if not self.connected and not self.connect(): return False, "Error conexión"
        try:
            cell = self.inventory_sheet.find(sku)
            if not cell: return False, f"SKU '{sku}' no encontrado."
            
            # Find quantity column index dynamic
            headers = self.inventory_sheet.row_values(1)
            try:
                col_idx = headers.index("quantity") + 1
            except:
                return False, "Columna 'quantity' no existe."
            
            curr_val = safe_float(self.inventory_sheet.cell(cell.row, col_idx).value)
            new_val = curr_val + delta
            
            if new_val < 0: return False, f"Stock insuficiente ({curr_val})."
            
            self.inventory_sheet.update_cell(cell.row, col_idx, new_val)
            return True, f"Stock actualizado: {curr_val} -> {new_val}"
            
        except Exception as e:
            return False, f"Error: {e}"

    def get_alerts(self):
        if not self.connected and not self.connect(): return None
        try:
            recs = self.inventory_sheet.get_all_records()
            crit = [r for r in recs if safe_float(r.get('quantity')) == 0 and safe_float(r.get('order_point')) > 0]
            warn = [r for r in recs if safe_float(r.get('quantity')) <= safe_float(r.get('order_point')) and safe_float(r.get('quantity')) > 0]
            return {"critical": crit, "warning": warn}
        except: return None
        
    def get_stats(self):
        """Devuelve estadísticas generales del inventario"""
        if not self.connected and not self.connect(): return None
        try:
            records = self.inventory_sheet.get_all_records()
            families = set(r.get('family') for r in records if r.get('family'))
            low_stock = sum(1 for r in records if safe_float(r.get('quantity')) <= safe_float(r.get('order_point')) and safe_float(r.get('order_point')) > 0)
            return {
                "total": len(records),
                "families": len(families),
                "low_stock": low_stock
            }
        except Exception as e:
            print(f"[ERROR] Stats failed: {e}")
            return None

    def search_product(self, query):
        if not self.connected and not self.connect(): return None
        try:
            records = self.inventory_sheet.get_all_records()
            results = []
            q = query.lower()
            for item in records:
                content = (f"{item.get('sku','')} {item.get('name','')} {item.get('description','')} {item.get('family','')}").lower()
                if q in content:
                    results.append(item)
                    if len(results) >= 5: break
            return results
        except: return None

sheets = GoogleSheetsService()

# --- Jobs ---
async def check_inventory_job(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id
    alerts = sheets.get_alerts()
    if not alerts: return
    
    crit, warn = alerts['critical'], alerts['warning']
    if not crit and not warn: return
    
    msg = "🚨 **ALERTA DE STOCK**\n"
    if crit: msg += f"🔴 {len(crit)} Agotados\n"
    if warn: msg += f"🟠 {len(warn)} Bajos\n"
    
    await context.bot.send_message(chat_id, msg, parse_mode='Markdown')

# --- Commands ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    cid = update.effective_chat.id
    
    jobs = context.job_queue.get_jobs_by_name(str(cid))
    if not jobs:
        context.job_queue.run_repeating(check_inventory_job, interval=CHECK_INTERVAL_MIN*60, first=10, chat_id=cid, name=str(cid))
    
    await update.message.reply_text(
        f"👋 ¡Hola {user}!\n"
        f"🏭 **Inventory Manager v4.0**\n\n"
        f"📥 `/in <sku> <cant>` - Entrada\n"
        f"📤 `/out <sku> <cant>` - Salida\n"
        f"🔎 `/buscar <sku>` - Consultar\n"
        f"📉 `/check` - Alertas de Stock\n"
        f"📊 `/resumen` - Estadísticas\n"
        f"❓ `/help` - Ver todos los comandos\n\n"
        f"✅ Monitoreo de alertas: Activo"
    , parse_mode='Markdown')

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra guía de uso"""
    help_text = (
        "📚 **Guía de Comandos v4.0**\n\n"
        "📦 **Gestión de Stock:**\n"
        "• `/in SKU CANT` - Suma cantidad al producto.\n"
        "• `/out SKU CANT` - Resta cantidad al producto.\n\n"
        "🔍 **Consultas:**\n"
        "• `/buscar TEXTO` - Búsqueda profunda por nombre, SKU o descripción.\n"
        "• `/check` - Muestra productos agotados o críticos.\n"
        "• `/resumen` - Estadísticas generales (total de ítems, familias).\n\n"
        "📝 **Bitácora:**\n"
        "• Cualquier mensaje que envíes (que no sea un comando) se guardará automáticamente en la pestaña 'notes' de tu hoja de cálculo."
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def cmd_resumen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra estadísticas generales"""
    stats = sheets.get_stats()
    if not stats:
        await update.message.reply_text("❌ No se pudieron cargar las estadísticas.")
        return
        
    msg = (
        "📈 **Resumen de Inventario**\n\n"
        f"📦 **Total items:** {stats['total']}\n"
        f"🗂️ **Categorías/Familias:** {stats['families']}\n"
        f"⚠️ **Alertas de stock:** {stats['low_stock']}\n\n"
        "Usa `/check` para ver el detalle o `/dashboard` para ver la gráfica."
    )
    await update.message.reply_text(msg, parse_mode='Markdown')

async def cmd_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra botón para abrir la Mini App"""
    print(f"[DEBUG] Executing /dashboard command for user {update.effective_user.first_name}")
    keyboard = [
        [InlineKeyboardButton("📊 Abrir Dashboard", web_app=WebAppInfo(url=DASHBOARD_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🖥️ **Panel de Control Visual**\n"
        "Haz clic en el botón de abajo para abrir la Mini App de inventario.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def cmd_in(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("📥 Uso: `/in <SKU> <CANTIDAD>`")
        return
    sku = context.args[0]
    try: qty = float(context.args[1])
    except: await update.message.reply_text("❌ Cantidad inválida"); return
    
    await update.message.reply_text("⏳ Procesando...")
    ok, msg = sheets.update_stock(sku, qty)
    await update.message.reply_text(f"{'✅' if ok else '❌'} {msg}")
    if ok: sheets.append_log([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), update.effective_user.first_name, f"IN {sku}", f"+{qty}"])

async def cmd_out(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("📤 Uso: `/out <SKU> <CANTIDAD>`")
        return
    sku = context.args[0]
    try: qty = float(context.args[1])
    except: await update.message.reply_text("❌ Cantidad inválida"); return

    await update.message.reply_text("⏳ Procesando...")
    ok, msg = sheets.update_stock(sku, -qty)
    await update.message.reply_text(f"{'✅' if ok else '❌'} {msg}")
    if ok: sheets.append_log([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), update.effective_user.first_name, f"OUT {sku}", f"-{qty}"])

async def cmd_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    alerts = sheets.get_alerts()
    if not alerts: await update.message.reply_text("✅ Todo OK"); return
    
    crit, warn = alerts['critical'], alerts['warning']
    if not crit and not warn: await update.message.reply_text("✅ Stock Saludable"); return
    
    msg = "📊 **Estado de Stock**\n"
    for i in crit: msg += f"🔴 {i.get('name')} (0)\n"
    for i in warn: msg += f"🟠 {i.get('name')} ({i.get('quantity')})\n"
    
    await update.message.reply_text(msg, parse_mode='Markdown')

async def cmd_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("🔎 `/buscar <algo>`"); return
    res = sheets.search_product(" ".join(context.args))
    if not res: await update.message.reply_text("🚫 No encontrado"); return
    
    for i in res:
        await update.message.reply_text(
            f"📦 *{i.get('sku')}* - {i.get('name')}\n"
            f"🔢 Stock: {i.get('quantity')} {i.get('unit','')}\n"
            f"📍 {i.get('location')}"
        , parse_mode='Markdown')

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"[DEBUG] Received message from {user.first_name}: {text}")
    
    # Append to log
    ok = sheets.append_log([ts, user.first_name, "MESSAGE", text])
    
    if ok:
        await update.message.reply_text(f"📝 Bitácora actualizada: {text[:20]}...")
    else:
        await update.message.reply_text("⚠️ No pude guardar en Google Sheets, pero recibí tu mensaje.")

def main():
    print("🤖 MANAGER v4.0 STARTING...")
    sheets.connect()
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    for cmd, handler in [
        ("start", start), ("in", cmd_in), ("out", cmd_out), 
        ("check", cmd_check), ("lowstock", cmd_check),
        ("buscar", cmd_search), ("resumen", cmd_resumen), ("help", cmd_help),
        ("dashboard", cmd_dashboard)
    ]:
        app.add_handler(CommandHandler(cmd, handler))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    print("✅ System Ready")
    app.run_polling()

if __name__ == '__main__':
    main()
