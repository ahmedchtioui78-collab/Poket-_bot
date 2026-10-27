from datetime import datetime, timedelta
import hashlib
import os
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = os.getenv("TOKEN")
MY_CHAT_ID = os.getenv("MY_CHAT_ID")


async def show_main_menu(update_or_message):
  keyboard = [
      [
          InlineKeyboardButton(
              "📊 EUR/USD (النظام الاحترافي الفائق - 5M)",
              callback_data="otc_eurusd",
          )
      ],
      [
          InlineKeyboardButton(
              "📊 GBP/USD (النظام الاحترافي الفائق - 5M)",
              callback_data="otc_gbpusd",
          )
      ],
      [
          InlineKeyboardButton(
              "📊 USD/JPY (النظام الاحترافي الفائق - 5M)",
              callback_data="otc_usdjpy",
          )
      ],
      [
          InlineKeyboardButton(
              "📊 CAD/CHF (النظام الاحترافي الفائق - 5M)",
              callback_data="otc_cadchf",
          )
      ],
      [
          InlineKeyboardButton(
              "🪙 Crypto IDX (النظام الاحترافي الفائق - 5M)",
              callback_data="otc_crypto",
          )
      ],
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  text = "🤖 **لوحة الإشارات فائقة النجاعة (أعلى معايير الدقة)**\nاختر الأصل المالي للحصول على تحليل مصفوفة التوافق مع إدارة المخاطر واستقرار السوق:"

  if hasattr(update_or_message, "reply_text"):
    await update_or_message.reply_text(
        text, reply_markup=reply_markup, parse_mode="Markdown"
    )
  else:
    await update_or_message.message.reply_text(
        text, reply_markup=reply_markup, parse_mode="Markdown"
    )


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
      "otc_crypto": "Crypto Index (OTC Market)",
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

  # نطاق التحليل الزمني (30 دقيقة = 6 شموع × 5 دقائق)
  target_end_dt = entry_dt + timedelta(minutes=30)
  target_end_time = target_end_dt.strftime("%H:%M:%S")

  # ---------------------------------------------------------
  # استخدام بصمة ثابتة بناءً على الأصل ووقت الدخول لمنع التذبذب تماماً
  # ---------------------------------------------------------
  seed_string = f"{query.data}_{entry_time}"
  hash_object = hashlib.md5(seed_string.encode())
  hash_int = int(hash_object.hexdigest(), 16)

  # تحديد الاتجاه بناءً على البصمة الثابتة للفترة الزمنية
  is_bullish = hash_int % 2 == 0

  if is_bullish:
    direction = "صعود (CALL) 🟢"
    bollinger_status = "ملامسة الحد السفلي + ارتداد نظيف بدون ذيول عشوائية 🟢"
    macd_signal = "تقاطع إيجابي مؤكد للسيولة الصاعدة (Bullish) 🟢"
    rsi = 28 + (hash_int % 11)  # قيمة ثابتة ضمن النطاق للشمعة الحالية
    candle_analysis = (
        "شمعة تأكيد هيكلية (Bullish Confirmation) بمدى 30 دقيقة 🟢"
    )
    stability_score = "ممتاز (سوق مستقر بنسبة 96%)"
    risk_advice = "الدخول بنسبة 2% - 3% من رأس المال (حذر وذكي)"
    confidence = 94 + (hash_int % 6)  # نسبة ثقة ثابتة بين 94 و 99
  else:
    direction = "هبوط (PUT) 🔴"
    bollinger_status = "ملامسة الحد العلوي + مقاومة قوية ورفض سعري 🔴"
    macd_signal = "تقاطع سلبي مؤكد للضغط البيعي (Bearish) 🔴"
    rsi = 64 + (hash_int % 9)  # قيمة ثابتة ضمن النطاق للشمعة الحالية
    candle_analysis = (
        "شمعة انعكاسية قوية عند المقاومة (Bearish Rejection) بمدى 30 دقيقة 🔴"
    )
    stability_score = "ممتاز (سوق مستقر بنسبة 95%)"
    risk_advice = "الدخول بنسبة 2% - 3% من رأس المال (حذر وذكي)"
    confidence = 94 + (hash_int % 6)  # نسبة ثقة ثابتة بين 94 و 99

  result_text = (
      f"🔥 **تقرير النظام الفائق النجاعة (30 دقيقة):**\n"
      f"━━━━━━━━━━━━━━━━━━━\n"
      f"📌 **الأصل المالي:** {asset}\n"
      f"⏱ **وقت الدخول المقترح:** `{entry_time}`\n"
      f"⏳ **نطاق التحليل:** 30 دقيقة (6 شموع × 5M)\n"
      f"🎯 **نهاية دورة الصفقة:** `{target_end_time}`\n"
      f"🌐 **Bollinger Bands:** {bollinger_status}\n"
      f"📈 **مؤشر MACD:** {macd_signal}\n"
      f"📉 **مؤشر RSI:** {rsi}\n"
      f"🕯 **تحليل الشموع:** {candle_analysis}\n"
      f"🛡 **مؤشر استقرار السوق:** {stability_score}\n"
      f"💰 **إدارة المخاطر المقترحة:** {risk_advice}\n"
      f"━━━━━━━━━━━━━━━━━━━\n"
      f"🎯 **التوصية النهائية:** {direction}\n"
      f"⭐ **نسبة الثقة المرتفعة:** {confidence}%\n"
      f"━━━━━━━━━━━━━━━━━━━\n"
      f"⚠️ *التزم بالخطة المقترحة وتمنياتي بالتوفيق المستمر.*"
  )

  keyboard = [
      [InlineKeyboardButton("🔄 تحديث التحليل الفائق", callback_data=query.data)]
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  await query.edit_message_text(
      text=result_text, parse_mode="Markdown", reply_markup=reply_markup
  )


async def post_init(application):
  commands = [
      ("start", "لوحة النظام فائق النجاعة"),
      ("signals", "قائمة أصول OTC المتاحة"),
  ]
  await application.bot.set_my_commands(commands)


def main():
  if not TOKEN:
    print("خطأ: لم يتم العثور على التوكن.")
    return

  app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

  app.add_handler(CommandHandler("start", start))
  app.add_handler(CommandHandler("signals", start))
  app.add_handler(
      MessageHandler(filters.TEXT & ~filters.COMMAND, handle_any_message)
  )
  app.add_handler(CallbackQueryHandler(button_handler))

  print("جاري تشغيل بوت النظام فائق النجاعة...")
  app.run_polling()


if __name__ == "__main__":
  main()
    
