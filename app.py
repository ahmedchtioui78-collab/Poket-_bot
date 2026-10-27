import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# سحب البيانات السرية بأمان من إعدادات المنصة (Render)
TOKEN = os.getenv("TOKEN")
MY_CHAT_ID = os.getenv("MY_CHAT_ID")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! بوت إشارات Pocket Option يعمل الآن بنجاح 24/7 على السحابة.")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # مثال على إرسال إشارة تداول
    signal_text = "📊 إشارة تداول جديدة:\nالزوج: EUR/USD\nالعملية: صعود (CALL)\nالوقت: 5 دقائق"
    await update.message.reply_text(signal_text)

def main():
    if not TOKEN:
        print("خطأ: لم يتم العثور على التوكن (TOKEN).")
        return

    # بناء تطبيق البوت
    app = ApplicationBuilder().token(TOKEN).build()

    # ربط الأوامر بالدوال
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    print("جاري تشغيل البوت...")
    app.run_polling()

if __name__ == "__main__":
    main()
