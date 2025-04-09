
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# === إعدادات ===
BOT_TOKEN = '8155689935:AAEtXriEC5n2QtLYm0Re59PgIUv7hBoxgRc'
TRACKING_ID = 'pandacoupons'
CHANNEL_URL = 'https://t.me/Pandacobouns'

# === قاعدة بيانات مؤقتة للغات المستخدمين ===
user_langs = {}

# === مكتبة الترجمة ===
translations = {
    "start_msg": {
        "ar": "👋 أهلاً بك! أرسل رابط منتج من AliExpress وسنقوم بتحويله لرابط مخفّض عبر الكوبونات.",
        "en": "👋 Welcome! Send a product link from AliExpress and we'll convert it to a discounted affiliate link."
    },
    "affiliate_result": {
        "ar": "🔗 رابط أفلييتك:\n{link}",
        "en": "🔗 Your affiliate link:\n{link}"
    },
    "not_aliexpress": {
        "ar": "❌ هذا ليس رابطاً من AliExpress.",
        "en": "❌ This is not an AliExpress link."
    },
    "help_msg": {
        "ar": "📌 *كيفية استخدام البوت:*\n\n- أرسل رابط منتج من AliExpress.\n- ستحصل على رابط أفلييت مخفّض.\n- تابع قناة العروض للمزيد من التخفيضات.",
        "en": "📌 *How to use the bot:*\n\n- Send an AliExpress product link.\n- You’ll get a discounted affiliate link.\n- Follow the offers channel for more deals."
    },
    "lang_changed": {
        "ar": "✅ تم تغيير اللغة إلى العربية.",
        "en": "✅ Language changed to English."
    }
}

# === دالة ترجمة بسيطة ===
def t(key, lang="ar", **kwargs):
    text = translations.get(key, {}).get(lang, "")
    return text.format(**kwargs)

# === تحويل رابط ===
def convert_to_affiliate_link(original_url):
    if "aliexpress.com" not in original_url:
        return None
    return f"https://s.click.aliexpress.com/deep_link.htm?tracking_id={TRACKING_ID}&dl_target_url={original_url}"

# === الأزرار ===
def get_main_keyboard(lang="ar"):
    if lang == "ar":
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 قناة العروض", url=CHANNEL_URL)],
            [InlineKeyboardButton("🌐 تغيير اللغة", callback_data="change_lang")],
            [InlineKeyboardButton("ℹ️ المساعدة", callback_data="help")]
        ])
    else:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Offers Channel", url=CHANNEL_URL)],
            [InlineKeyboardButton("🌐 Change Language", callback_data="change_lang")],
            [InlineKeyboardButton("ℹ️ Help", callback_data="help")]
        ])

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_langs[user_id] = "ar"
    await update.message.reply_text(
        t("start_msg", "ar"),
        reply_markup=get_main_keyboard("ar")
    )

# === استقبال الروابط ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = user_langs.get(user_id, "ar")
    message = update.message.text

    link = convert_to_affiliate_link(message)
    if link is None:
        await update.message.reply_text(t("not_aliexpress", lang))
    else:
        await update.message.reply_text(t("affiliate_result", lang, link=link))

# === تغيير اللغة ===
async def change_lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    current_lang = user_langs.get(user_id, "ar")
    new_lang = "en" if current_lang == "ar" else "ar"
    user_langs[user_id] = new_lang

    await query.answer()
    await query.edit_message_text(t("lang_changed", new_lang), reply_markup=get_main_keyboard(new_lang))

# === المساعدة ===
async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    lang = user_langs.get(user_id, "ar")
    await query.answer()
    await query.edit_message_text(t("help_msg", lang), parse_mode="Markdown", reply_markup=get_main_keyboard(lang))

# === تشغيل البوت ===
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(change_lang_callback, pattern="change_lang"))
    app.add_handler(CallbackQueryHandler(help_callback, pattern="help"))

    print("✅ البوت يعمل الآن...")
    app.run_polling()
