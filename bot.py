import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

print("Script started")  # Debug print

TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    logger.error("TOKEN environment variable is not set!")
    exit(1)
else:
    logger.info("TOKEN found")

GROUP_CHAT_ID = "-1003072701582"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Start command received")
    keyboard = [['Kenyan', 'International']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text('Welcome! Are you paying from Kenya or internationally?', reply_markup=reply_markup)

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text
    user_id = update.message.from_user.id
    logger.info(f"User chose: {user_choice}")

    if user_choice == 'Kenyan':
        await update.message.reply_text("M-Pesa option will be implemented here. Please enter your M-Pesa phone number:")
    elif user_choice == 'International':
        await update.message.reply_text("International payment option will be implemented here.")
    else:
        await update.message.reply_text("Invalid choice. Please select Kenyan or International.")

def main():
    logger.info("Initializing application...")
    application = Application.builder().token(TOKEN).build()
    logger.info("Application built")

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice))
    logger.info("Handlers added")

    logger.info("Starting polling...")
    application.run_polling()
    logger.info("Bot is running...")

if __name__ == '__main__':
    main()
