import asyncio
import threading

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from special_scanner import scan_live_matches

BOT_TOKEN = "8745289261:AAE_YFIAY13QomJtQ0rBqXRbNc1pXCmsrgQ"

# Scanner status
scanner_running = False


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🤖 LIVE FOOTBALL AI

Komandalar:

/special_on → Special AI başlat
/special_off → Special AI dayandır
/status → AI status
/help → Bütün komandalar
"""

    await update.message.reply_text(text)


# =========================
# HELP
# =========================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
📚 BÜTÜN KOMANDALAR

/special_on
→ Auto AI Scanner ON

/special_off
→ Auto AI Scanner OFF

/status
→ Scanner status

/help
→ Komanda listəsi
"""

    await update.message.reply_text(text)


# =========================
# STATUS
# =========================

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global scanner_running

    if scanner_running:
        text = "🟢 Special AI aktivdir"
    else:
        text = "🔴 Special AI dayandırılıb"

    await update.message.reply_text(text)


# =========================
# SPECIAL ON
# =========================

def run_scanner():

    asyncio.run(scan_live_matches())


async def special_on(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global scanner_running

    if scanner_running:

        await update.message.reply_text(
            "🟡 Special AI artıq işləyir"
        )

        return

    scanner_running = True

    thread = threading.Thread(
        target=run_scanner
    )

    thread.start()

    await update.message.reply_text(
        "🟢 Special AI başladıldı"
    )


# =========================
# SPECIAL OFF
# =========================

async def special_off(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global scanner_running

    scanner_running = False

    await update.message.reply_text(
        "🔴 Special AI dayandırıldı"
    )


# =========================
# APP
# =========================

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))

app.add_handler(CommandHandler("special_on", special_on))
app.add_handler(CommandHandler("special_off", special_off))

app.add_handler(CommandHandler("status", status))

print("🤖 TELEGRAM AI BOT STARTED...")

app.run_polling()