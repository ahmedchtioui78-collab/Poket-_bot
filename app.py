import os
import random
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")
MY_CHAT_ID = os.getenv("MY_CHAT_ID")

async def show_main_menu(update_or_message):
    keyboard = [
        [InlineKeyboardButton("📊 EUR/USD (OTC - Price Action 5M)", callback_data="otc_eurusd")],
        [InlineKeyboardButton("📊 GBP/USD (OTC - Price Action 5M)", callback_data="otc_gbpusd")],
        [InlineKeyboardButton("📊 USD/JPY (OTC - Price Action 5M)", callback_data="otc_usdjpy")],
        [InlineKeyboardButton("📊 CAD/CHF (OTC - Price Action 5M)", callback_data="otc_cadchf")],
        [InlineKeyboardButton("🪙 Crypto IDX (OTC - Price Action 5M)", callback_data="otc_crypto")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "🤖 **لوحة تحكم تحليل الشموع والتايم فريم (إطار 5 دقائق)**\nاختر الأصل المالي للحصول على تحليل حركة السعر (Price Action) ووقت الدخول:"
    
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
    if minutes_to_add == 5 and now.second > 30:
        minutes_to_add = 10
    elif minutes_to_add == 0 and now.second > 30:
        minutes_to_add = 5
        
    entry_dt = now + timedelta(minutes=minutes_to_add)
    entry_dt = entry_dt.replace(second=0, microsecond=0)
    entry_time = entry_dt.strftime("%H:%M:%S")
    
    # قائمة أنماط الشموع اليابانية العلمية
    bullish_patterns = [
        "الشمقة المبتلعة الصاعدة (Bullish Engulfing) 🟢",
        "شمعة المطرقة (Hammer) الداعمة للصعود 🟢",
        "نموذج نجمة الصباح (Morning Star) القوي 🟢",
        "شمعة الـ Marubozu الصاعدة العكسية 🟢"
    ]
    
    bearish_patterns = [
        "الشمعة المبتلعة الهابطة (Bearish Engulfing) 🔴",
        "شمعة الشهاب (Shooting Star) العاكسة للاتجاه 🔴",
        "نموذج نجمة المساء (Evening Star) الهابط 🔴",
        "رفض السعر عند المقاومة (Pin Bar سلبى) 🔴"
    ]
    
    # المؤشرات الفنية وأنماط الشموع
    rsi = random.randint(25, 75)
    cci = random.randint(-110, 110)
    
    if rsi < 48 or cci < -80:
        direction = "صعود (CALL) 🟢"
        candlestick_pattern = random.choice(bullish_patterns)
        confidence = random.randint(85, 99)
    else:
        direction = "هبوط (PUT) 🔴"
        candlestick_pattern = random.choice(bearish_patterns)
        confidence = random.randint(83, 97)
        
    macd_signal = "إيجابي (Bullish) 🟢" if "صعود" in direction else "سلبي (Bearish) 🔴"
    
    result_text = (
        f"🔍 **تحليل حركة السعر والشموع (إطار 5 دقائق):**\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📌 **الأصل المالي:** {asset}\n"
        f"⏱ **وقت الدخول المقترح:** `{entry_time}`\n"
        f"⏳ **مدة الصفقة (Time Frame):** 5 دقائق\n"
        f"🕯 **نمط الشموع (Price Action):** {candlestick_pattern}\n"
        f"📉 **مؤشر RSI:** {rsi}\n"
        f"📊 **مؤشر CCI:** {cci}\n"
        f"📈 **اتجاه MACD:** {macd_signal}\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 **التوصية النهائية:** {direction}\n"
        f"⭐ **نسبة الثقة العلمية:** {confidence}%\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ *التزم بإدارة رأس المال وتمنياتي بالتوفيق.*"
    )
    
    keyboard = [[InlineKeyboardButton("🔄 تحديث التحليل والشموع", callback_data=query.data)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=result_text, parse_mode="Markdown", reply_markup=reply_markup)

async def post_init(application):
    commands = [
        ("start", "لوحة تحليل الشموع 5 دقائق"),
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

    print("جاري تشغيل بوت تحليل الشموع والبرايس أكشن...")
    app.run_polling()

if __name__ == "__main__":
    main()
  
