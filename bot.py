import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

telegram_bot_token = "6264357965:AAH10GjcRl8iQ0sW1pavXDdAckvAMXE5Tpk"

updater = Updater()
dispatcher = updater.dispatcher


def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Hello World")


dispatcher.add_handler(CommandHandler("start", start))
updater.start_polling()