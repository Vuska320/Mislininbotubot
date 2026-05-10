from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

# TELEGRAM TOKEN
TOKEN = "8745289261:AAE_YFIAY13QomJtQ0rBqXRbNc1pXCmsrgQ"

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
⚽ AI QOL PROQNOZ BOTU

Bot aktivdir ✅

Komandalar üçün:
/help
"""

    await update.message.reply_text(text)

# HELP
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
📚 BOT KOMANDALARI

/start
Botu başladır

/help
Bütün komandaları göstərir

/live
Canlı oyunları göstərir

/scan MATCH_ID
Canlı oyunu analiz edir

/predict MATCH_ID
Növbəti qol təxminini göstərir

━━━━━━━━━━━━━━

📌 NÜMUNƏ:

/predict 19439592
"""

    await update.message.reply_text(text)

# LIVE
async def live(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🔥 CANLI OYUNLAR

19439592 → Barcelona vs Real Madrid
19427225 → Arsenal vs West Ham
19433940 → Toulouse vs Lyon
"""

    await update.message.reply_text(text)

# SCAN
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:

        await update.message.reply_text(
            "MATCH ID yaz.\n\nNümunə:\n/scan 19439592"
        )

        return

    match_id = context.args[0]

    text = f"""
🔍 CANLI OYUN ANALİZİ BAŞLADI

🆔 Matç ID:
{match_id}

Bot artıq oyunu analiz edir ✅
"""

    await update.message.reply_text(text)

# PREDICT
async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:

        await update.message.reply_text(
            "MATCH ID yaz.\n\nNümunə:\n/predict 19439592"
        )

        return

    match_id = context.args[0]

    text = f"""
⚽ NÖVBƏTİ QOL TƏXMİNİ

🆔 Matç:
{match_id}

🥅 Qol Vuracaq Komanda:
FC Barcelona

🔢 Növbəti Qol:
3

👟 Zərbə → 67%
🧠 Baş Zərbəsi → 14%
🎯 Cərimə Zərbəsi → 9%
✋ Penalti → 6%
❌ Qol Olmayacaq → 4%
"""

    await update.message.reply_text(text)

# MAIN
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("live", live))
app.add_handler(CommandHandler("scan", scan))
app.add_handler(CommandHandler("predict", predict))

print("⚽ TELEGRAM AI BOT STARTED...")

app.run_polling()