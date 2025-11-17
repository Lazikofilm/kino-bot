from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os

# =================== SOZLAMALAR ===================
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8216534410:AAG51USpVGtZCJU1gGLIQaO8GVaOH8NM0mE')
CHANNEL = os.environ.get('CHANNEL', '@baccaraclub')
ADMIN_ID = 6086951633
# ====================================================

# Obuna bo‘lgan foydalanuvchilarni saqlash
user_subscribed = set()

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Obuna bo‘lish", url=f"https://t.me/{CHANNEL[1:]}")],
        [InlineKeyboardButton("✅ Tekshirish", callback_data='check')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Salom! 👋\nBotdan foydalanish uchun kanalga obuna bo‘ling:\n{CHANNEL}\n\nObunani tasdiqlash uchun tugmani bosing",
        reply_markup=reply_markup
    )

# Tugma bosilganda
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user_subscribed.add(user_id)
    await query.edit_message_text("✔ Obuna tasdiqlandi!\n🎬 Kino kodini kiriting:")

# Foydalanuvchi xabar yuborganda
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_subscribed:
        await update.message.reply_text(
            "❌ Siz hali kanalga obuna bo‘lmagansiz!\nIltimos, yuqoridagi tugma orqali obuna bo‘ling"
        )
        return
    code = update.message.text.strip()
    # Kodga mos video yuborish
    if code == "100":
        await update.message.reply_video("BAACAgUAAxkBAAEY9N1pGjy1esI_EwWRrrE9vntuxEBYZgACnxEAAoVisVWAwV3gu8K3xDYE")
    else:
        await update.message.reply_text("❌ Kod xato! Iltimos, to‘g‘ri kod kiriting.")

# BOTni ishga tushirish
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
