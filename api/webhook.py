import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("8563744395:AAH40qsGbnA6XrCpmTpBZb5eg_pVBy8eYgM")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /info @username")
        return

    username = context.args[0]

    try:
        chat = await context.bot.get_chat(username)
        await update.message.reply_text(
            f"Username: {chat.username}\nUser ID: {chat.id}"
        )
    except Exception:
        await update.message.reply_text("Unable to fetch user ID.")

async def handler(request):
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("info", info))

    update = Update.de_json(await request.json(), app.bot)
    await app.process_update(update)

    return {"status": "ok"}
