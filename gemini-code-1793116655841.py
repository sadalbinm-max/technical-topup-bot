import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# --- CONFIGURATION ---
BOT_TOKEN = "8907935221:AAGyjt_tWbQ6ldF0RWX3iaHSB3BIZ-9nk5A"
CHANNEL_ID = "@technicaltopupstore"

WAITING_FOR_REVIEW = 1

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    welcome_text = (
        f"স্বাগতম **TECHNICAL TOPUP STORE**-এ, {user_first_name}! 👋\n\n"
        "আমাদের সার্ভিস সম্পর্কে আপনার মূল্যবান রিভিউ দিতে নিচের বাটনে ক্লিক করুন:"
    )
    keyboard = [[InlineKeyboardButton("✍️ Write a Review", callback_data="start_review")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "start_review":
        await query.edit_message_text("অনুগ্রহ করে আপনার রিভিউটি মেসেজ হিসেবে লিখে পাঠান:")
        return WAITING_FOR_REVIEW

async def receive_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    review_text = update.message.text

    username_str = f" (@{user.username})" if user.username else ""
    user_info = f"{user.full_name}{username_str}"

    channel_post = (
        "⭐ **TECHNICAL TOPUP STORE - Customer Review** ⭐\n\n"
        f"💬 \"{review_text}\"\n\n"
        f"👤 **Customer:** {user_info}"
    )

    try:
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=channel_post,
            parse_mode="Markdown"
        )
        await update.message.reply_text("✅ আপনার রিভিউটি সফলভাবে **TECHNICAL TOPUP STORE** চ্যানেলে পোস্ট করা হয়েছে! ধন্যবাদ ❤️")
    except Exception as e:
        await update.message.reply_text("❌ রিভিউ পোস্ট করতে সমস্যা হয়েছে। দয়া করে বটকে চ্যানেলের অ্যাডমিন করা আছে কিনা চেক করুন।")
        logging.error(f"Error posting review: {e}")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("রিভিউ প্রক্রিয়াটি বাতিল করা হয়েছে।")
    return ConversationHandler.END

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CallbackQueryHandler(button_handler, pattern="^start_review$")
        ],
        states={
            WAITING_FOR_REVIEW: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_review)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    
    print("TECHNICAL TOPUP STORE Review Bot started...")
    application.run_polling()

if __name__ == "__main__":
    main()