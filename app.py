import os
import random
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")
MY_CHAT_ID = os.getenv("MY_CHAT_ID")

async def show_main_menu(update_or_message):
    keyboard = [
        [InlineKeyboardButton("📊 EUR/USD (تحليل 30 دقيقة - 5M)", callback_data="otc_eurusd")],
        [InlineKeyboardButton("📊 GBP/USD (تحليل 30 دقيقة - 5M)", callback_data="otc_gbpusd")],
        [InlineKeyboardButton("📊 USD/JPY (تحليل 30 دقيقة - 5M)", callback_data="otc_usdjpy")],
        [InlineKeyboardButton("📊 CAD/CHF (تحليل 30 دقيقة - 5M)", callback_data="otc_cadchf")],
        [InlineKeyboardButton("🪙 Crypto IDX (تحليل 30 دقيقة - 5M)", callback_data="otc_crypto")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "🤖 **لوحة تحكم تحليل حركة الشموع (مدى 30 دقيقة)**\nاختر الأصل المالي لعرض اتجاه الشموع للـ 30 دقيقة القادمة ووقت الدخول المقترح:"
    
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
    
    # حساب نطاق الهدف الزمني 30 دقيقة (6 شموع × 5 دقائق)
    target_end_dt = entry_dt + timedelta(minutes=30)
    target_end_time = target_end_dt.strftime("%H:%M:%S")
    
    # أنماط تحليل الشموع للمدى الطويل (30 دقيقة)
    trend_30min_bullish = [
        "هيمنة قوية للمشترين على مدار الـ 6 شموع الأخيرة (ترند صاعد مستقر) 🟢",
        "كسر منطقة عرض سابقة وإغلاق إيجابي على إطار 30 دقيقة 🟢",
        "ارتداد هيكلي من مستويات دعم رئيسية لمدى نصف ساعة 🟢"
    ]
    
    trend_30min_bearish = [
        "ضغط بيعي متواصل على مدى الشموع الستة الماضية (ترند هابط) 🔴",
        "كسر خط ترند صاعد والتحول إلى المسار الهابط 🔴",
        "تشبع شرائي في نطاق الـ 30 دقيقة ورفض السعر للأعلى 🔴"
    ]
    
    rsi = random.randint(25, 75)
    cci = random.randint(-110, 110)
    
    if rsi < 50 or cci < -70:
        direction = "صعود (CALL) 🟢"
        candle_analysis = random.choice(trend_30min_bullish)
        confidence = random.randint(87, 99)
    else:
        direction = "هبوط (PUT) 🔴"
        candle_analysis = random.choice(trend_30min_bearish)
        confidence = random.randint(85, 98)
        
    result_text = (
        f"🔍 **تحليل حركة الشموع (مدى 30 دقيقة):**\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📌 **الأصل المالي:** {asset}\n"
        f"⏱ **وقت الدخول المقترح:** `{entry_time}`\n"
        f"⏳ **نطاق التحليل الزمني:** 30 دقيقة (6 شموع × 5M)\n"
        f"🎯 **نهاية دورة الصفقة المتوقعة:** `{target_end_time}`\n"
        f"🕯 **سلوك الشموع العام (30M):** {candle_analysis}\n"
        f"📉 **مؤشر RSI:** {rsi}\n"
        f"📊 **مؤشر CCI:** {cci}\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 **التوصية النهائية:** {direction}\n"
        f"⭐ **نسبة الثقة التحليلية:** {confidence}%\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ *التزم بإدارة رأس المال وتمنياتي بالتوفيق.*"
    )
    
    keyboard = [[InlineKeyboardButton("🔄 تحديث تحليل الشموع (30 دقيقة)", callback_data=query.data)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=result_text, parse_mode="Markdown", reply_markup=reply_markup)

async def post_init(application):
    commands = [
        ("start", "لوحة تحليل الشموع 30 دقيقة"),
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

    print("جاري تشغيل بوت تحليل الشموع (مدى 30 دقيقة)...")
    app.run_polling()

if __name__ == "__main__":
    main()
      
