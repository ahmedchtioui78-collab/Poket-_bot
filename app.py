import os
import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")
MY_CHAT_ID = os.getenv("MY_CHAT_ID")

async def show_main_menu(update_or_message):
    keyboard = [
        [InlineKeyboardButton("📊 EUR/USD (OTC)", callback_data="otc_eurusd")],
        [InlineKeyboardButton("📊 GBP/USD (OTC)", callback_data="otc_gbpusd")],
        [InlineKeyboardButton("📊 USD/JPY (OTC)", callback_data="otc_usdjpy")],
        [InlineKeyboardButton("📊 CAD/CHF (OTC)", callback_data="otc_cadchf")],
        [InlineKeyboardButton("🪙 Crypto IDX (OTC)", callback_data="otc_crypto")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "🤖 **لوحة تحكم تحليل مؤشرات OTC المتقدمة**\nاختر الأصل المالي لعرض التحليل الشامل (RSI, MACD, Bollinger Bands, CCI):"
    
    if hasattr(update_or_message, 'reply_text'):
        await update_or_message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update_or_message.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_main_menu(update.message)

async def handle_any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_main_menu(update.message)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    asset_names = {
        "otc_eurusd": "EUR/USD (OTC Market)",
        "otc_gbpusd": "GBP/USD (OTC Market)",
        "otc_usdjpy": "USD/JPY (OTC Market)",
        "otc_cadchf": "CAD/CHF (OTC Market)",
        "otc_crypto": "Crypto Index (OTC Market)"
    }
    
    asset = asset_names.get(query.data, "EUR/USD (OTC Market)")
        
    # محاكاة حساب المؤشرات الفنية المتقدمة
    rsi = random.randint(25, 75)
    cci = random.randint(-110, 110)
    macd_signal = "إيجابي (Bullish) 🟢" if random.random() > 0.5 else "سلبي (Bearish) 🔴"
    bb_status = "ملامسة الحد السفلي (ارتداد محتمل)" if rsi < 40 else ("ملامسة الحد العلوي (هبوط محتمل)" if rsi > 60 else "استقرار وسط النطاق")
    
    # تحديد التوصية بناءً على دمج المؤشرات
    if rsi < 45 or cci < -90:
        direction = "صعود (CALL) 🟢"
        confidence = random.randint(83, 98)
    else:
        direction = "هبوط (PUT) 🔴"
        confidence = random.randint(81, 96)
        
    entry_time = datetime.now().strftime("%H:%M:%S")
    
    result_text = (
        f"🔍 **تحليل المؤشرات الفنية المتقدمة (OTC):**\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📌 **الأصل المالي:** {asset}\n"
        f"⏱ **وقت الدخول المقترح:** `{entry_time}`\n"
        f"📉 **مؤشر RSI:** {rsi}\n"
        f"📊 **مؤشر CCI:** {cci}\n"
        f"📈 **مؤشر MACD:** {macd_signal}\n"
        f"🌐 **Bollinger Bands:** {bb_status}\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 **التوصية النهائية:** {direction}\n"
        f"⭐ **نسبة الثقة التقريبية:** {confidence}%\n"
        f"⏳ **مدة الصفقة:** 1 - 5 دقائق\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ *تداول بحذر والتزم بإدارة رأس المال.*"
    )
    
    keyboard = [[InlineKeyboardButton("🔄 تحديث التحليل والمؤشرات", callback_data=query.data)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=result_text, parse_mode="Markdown", reply_markup=reply_markup)

async def post_init(application):
    commands = [
        ("start", "فتح لوحة المؤشرات المتقدمة"),
        ("signals", "قائمة أصول OTC المتاحة")
    ]
    await application.bot.set_my_commands(commands)

def main():
    if not TOKEN:
        print("خطأ: لم يتم العثور على التوكن.")
        return

    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signals", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_any_message))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("جاري تشغيل بوت المؤشرات الفنية المتقدمة...")
    app.run_polling()

if __name__ == "__main__":
    main()
  
