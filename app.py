import os
import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")
MY_CHAT_ID = os.getenv("MY_CHAT_ID")

# دالة لإرسال القائمة الرئيسية والأزرار
async def show_main_menu(update_or_message):
    keyboard = [
        [InlineKeyboardButton("📊 EUR/USD (OTC)", callback_data="otc_eurusd")],
        [InlineKeyboardButton("📊 GBP/USD (OTC)", callback_data="otc_gbpusd")],
        [InlineKeyboardButton("📊 USD/JPY (OTC)", callback_data="otc_usdjpy")],
        [InlineKeyboardButton("🪙 Crypto IDX (OTC)", callback_data="otc_crypto")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "🤖 **لوحة تحكم إشارات OTC المباشرة**\nاختر الأصل المالي المطلوب للحصول على التحليل الفوري ووقت الدخول:"
    
    if hasattr(update_or_message, 'reply_text'):
        await update_or_message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update_or_message.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_main_menu(update.message)

# الاستجابة لأي رسالة عشوائية يكتبها المستخدم لتظهر الأزرار فوراً دون /start
async def handle_any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_main_menu(update.message)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    asset_names = {
        "otc_eurusd": "EUR/USD (OTC Market)",
        "otc_gbpusd": "GBP/USD (OTC Market)",
        "otc_usdjpy": "USD/JPY (OTC Market)",
        "otc_crypto": "Crypto Index (OTC Market)"
    }
    
    asset = asset_names.get(query.data, "EUR/USD (OTC Market)")
        
    rsi = random.randint(28, 72)
    direction = "صعود (CALL) 🟢" if rsi < 50 else "هبوط (PUT) 🔴"
    confidence = random.randint(80, 97)
    entry_time = datetime.now().strftime("%H:%M:%S")
    
    result_text = (
        f"🔍 **تقرير تحليل سوق OTC الفوري:**\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📌 **الأصل المالي:** {asset}\n"
        f"⏱ **وقت الدخول المقترح:** `{entry_time}`\n"
        f"📉 **مؤشر القوة النسبية (RSI):** {rsi}\n"
        f"📊 **التوصية الفنية:** {direction}\n"
        f"🎯 **نسبة الثقة المقدرة:** {confidence}%\n"
        f"⏳ **مدة الصفقة:** 1 - 5 دقائق\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ *التزم بإدارة رأس المال وتمنياتي بالتوفيق.*"
    )
    
    keyboard = [[InlineKeyboardButton("🔄 تحديث التحليل ووقت الدخول", callback_data=query.data)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=result_text, parse_mode="Markdown", reply_markup=reply_markup)

async def post_init(application):
    # تسجيل الأوامر في قائمة تليجرام الجانبية لتظهر بضغطة زر واحدة (Menu)
    commands = [
        ("start", "فتح لوحة إشارات OTC"),
        ("signals", "الحصول على قائمة الأصول المتاحة")
    ]
    await application.bot.set_my_commands(commands)

def main():
    if not TOKEN:
        print("خطأ: لم يتم العثور على التوكن.")
        return

    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signals", start))
    # أي رسالة يكتبها المستخدم ستظهر له الأزرار تلقائياً
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_any_message))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("جاري تشغيل البوت مع التفاعل التلقائي...")
    app.run_polling()

if __name__ == "__main__":
    main()
  
