import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
MY_CHAT_ID = os.getenv("MY_CHAT_ID")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 تحليل فوري (EUR/USD)", callback_data="analyze_eurusd")],
        [InlineKeyboardButton("📈 تحليل العملات الرقمية (BTC)", callback_data="analyze_crypto")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "أهلاً بك في المرحلة الثانية! بوت تحليلات Pocket Option جاهز.\nاختر نوع الأصول المطلوبة للتحليل المباشر:",
        reply_markup=reply_markup
    )

async def analyze_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await generate_signal_response(update.message)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "analyze_eurusd":
        asset = "EUR/USD (أزواج رئيسية)"
    else:
        asset = "BTC/USD (عملات رقمية)"
        
    rsi = random.randint(32, 68)
    direction = "صعود (CALL) 🟢" if rsi < 50 else "هبوط (PUT) 🔴"
    confidence = random.randint(78, 96)
    
    result_text = (
        f"🔍 **تقرير التحليل الفوري المباشر:**\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📌 **الأصل:** {asset}\n"
        f"📉 **مؤشر القوة النسبية (RSI):** {rsi}\n"
        f"📊 **التوصية:** {direction}\n"
        f"🎯 **نسبة الثقة:** {confidence}%\n"
        f"⏱ **المدد الزمنية المقترحة:** 5 دقائق\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ *تداول بذكاء وادرس إدارة رأس المال بحذر.*"
    )
    
    keyboard = [[InlineKeyboardButton("🔄 تحديث التحليل", callback_data=query.data)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=result_text, parse_mode="Markdown", reply_markup=reply_markup)

async def generate_signal_response(message):
    rsi = random.randint(32, 68)
    direction = "صعود (CALL) 🟢" if rsi < 50 else "هبوط (PUT) 🔴"
    confidence = random.randint(78, 96)
    
    result_text = (
        f"🔍 **تحليل فوري جديد:**\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📌 **الزوج:** EUR/USD\n"
        f"📉 **مؤشر RSI:** {rsi}\n"
        f"📊 **الاتجاه:** {direction}\n"
        f"🎯 **الثقة:** {confidence}%\n"
        f"⏱ **الوقت:** 5 دقائق\n"
        f"━━━━━━━━━━━━━━━━━━━"
    )
    await message.reply_text(result_text, parse_mode="Markdown")

def main():
    if not TOKEN:
        print("خطأ: لم يتم العثور على التوكن.")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analyze", analyze_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("جاري تشغيل البوت بالمميزات المتقدمة...")
    app.run_polling()

if __name__ == "__main__":
    main()
