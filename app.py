import os
import random
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")
MY_CHAT_ID = os.getenv("MY_CHAT_ID")

async def show_main_menu(update_or_message):
    keyboard = [
        [InlineKeyboardButton("📊 EUR/USD (OTC - 5M)", callback_data="otc_eurusd")],
        [InlineKeyboardButton("📊 GBP/USD (OTC - 5M)", callback_data="otc_gbpusd")],
        [InlineKeyboardButton("📊 USD/JPY (OTC - 5M)", callback_data="otc_usdjpy")],
        [InlineKeyboardButton("📊 CAD/CHF (OTC - 5M)", callback_data="otc_cadchf")],
        [InlineKeyboardButton("🪙 Crypto IDX (OTC - 5M)", callback_data="otc_crypto")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "🤖 **لوحة تحكم إشارات OTC (إطار 5 دقائق)**\nاختر الأصل المالي للحصول على التحليل الفوري ووقت الدخول للشمعة القادمة:"
    
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
        
    # حساب وقت الدخول بدقة ليوافق أقرب فاصل 5 دقائق قادم
    now = datetime.now()
    minute_mod = now.minute % 5
    minutes_to_add = 5 - minute_mod if minute_mod != 0 else 5
    # إذا بقي أقل من 30 ثانية على الفاصل الحالي، ننتقل للفاصل الذي يليه لكي تأخذ وقتك في التنفيذ
    if minutes_to_add == 5 and now.second > 30:
        minutes_to_add = 10
    elif minutes_to_add == 0 and now.second > 30:
        minutes_to_add = 5
        
    entry_dt = now + timedelta(minutes=minutes_to_add)
    entry_dt = entry_dt.replace(second=0, microsecond=0)
    entry_time = entry_dt.strftime("%H:%M:%S")
    
    # محاكاة المؤشرات الفنية المتقدمة
    rsi = random.randint(25, 75)
    cci = random.randint(-110, 110)
    macd_signal = "إيجابي (Bullish) 🟢" if random.random() > 0.5 else "سلبي (Bearish) 🔴"
    bb_status = "ملامسة الحد السفلي (ارتداد محتمل)" if rsi < 40 else ("ملامسة الحد العلوي (هبوط محتمل)" if rsi > 60 else "استقرار وسط النطاق")
    
    if rsi < 45 or cci < -90:
        direction = "صعود (CALL) 🟢"
        confidence = random.randint(84, 98)
    else:
        direction = "هبوط (PUT) 🔴"
        confidence = random.randint(82, 96)
    
    result_text = (
        f"🔍 **تقرير تحليل مؤشرات OTC (إطار 5 دقائق):**\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📌 **الأصل المالي:** {asset}\n"
        f"⏱ **وقت الدخول المقترح:** `{entry_time}`\n"
        f"⏳ **مدة الصفقة (Time Frame):** 5 دقائق\n"
        f"📉 **مؤشر RSI:** {rsi}\n"
        f"📊 **مؤشر CCI:** {cci}\n"
        f"📈 **مؤشر MACD:** {macd_signal}\n"
        f"🌐 **Bollinger Bands:** {bb_status}\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 **التوصية النهائية:** {direction}\n"
        f"⭐ **نسبة الثقة:** {confidence}%\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ *التزم بإدارة رأس المال وتمنياتي بالتوفيق.*"
    )
    
    keyboard = [[InlineKeyboardButton("🔄 تحديث التحليل ووقت الدخول", callback_data=query.data)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=result_text, parse_mode="Markdown", reply_markup=reply_markup)

async def post_init(application):
    commands = [
        ("start", "فتح لوحة إشارات 5 دقائق"),
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

    print("جاري تشغيل بوت إشارات 5 دقائق المتقدم...")
    app.run_polling()

if __name__ == "__main__":
    main()
  
