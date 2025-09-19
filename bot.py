import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncio

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Your bot token from BotFather
TOKEN = "8369143504:AAEDHgc_tB-GVniJjS32SVSF5pbCOli7oK8"
# Your group chat ID (you'll get this later)
GROUP_CHAT_ID = "-1003072701582"  # Example placeholder, will update

# Store user payment times (in a real bot, use a database)
user_payment_times = {}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['Kenyan', 'International']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text('Welcome! Are you paying from Kenya or internationally?', reply_markup=reply_markup)

# Handle user's choice
async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text
    user_id = update.message.from_user.id

    if user_choice == 'Kenyan':
        await update.message.reply_text("M-Pesa option will be implemented here. Please enter your M-Pesa phone number:")
    elif user_choice == 'International':
        await update.message.reply_text("International payment option will be implemented here.")
    else:
        await update.message.reply_text("Invalid choice. Please select Kenyan or International.")

# Function to kick user after 12 hours
async def kick_user(user_id: int):
    try:
        await application.bot.ban_chat_member(chat_id=GROUP_CHAT_ID, user_id=user_id)
        await application.bot.unban_chat_member(chat_id=GROUP_CHAT_ID, user_id=user_id)
        logger.info(f"Kicked user {user_id} after 12 hours.")
    except Exception as e:
        logger.error(f"Failed to kick user {user_id}: {e}")

# Main function
def main():
    global application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice))

    # Start the Bot
    application.run_polling()
    logger.info("Bot is running...")

if __name__ == '__main__':

    main()
