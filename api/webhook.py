import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.environ["8563744395:AAF3db-clfpIkOj1OIba1lBFA8QpTVVNnLI"]

# Create app once (important for serverless)
app = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send:\n/info @username\n\nI will return the Telegram User ID."
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /info @username")
        return

    username = context.args[0]

    if not username.startswith("@"):
        await update.message.reply_text("Username must start with @")
        return

    try:
        chat = await context.bot.get_chat(username)
        await update.message.reply_text(f"User ID: {chat.id}")
    except Exception:
        await update.message.reply_text("Invalid, private, or non-existent username")

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("info", info))

async def handler(request):
    # REQUIRED lifecycle calls
    if not app.running:
        await app.initialize()
        await app.start()

    data = await request.json()
    update = Update.de_json(data, app.bot)
    await app.process_update(update)

    return {"ok": True}
