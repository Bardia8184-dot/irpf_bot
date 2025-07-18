from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import config

BOT_TOKEN = config.BOT_TOKEN
CHANNEL_USERNAME = config.CHANNEL_USERNAME
ADMIN_USERNAME = config.ADMIN_USERNAME

user_states = {}

def check_membership(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    member = context.bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
    return member.status in ["member", "administrator", "creator"]

def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏆 رتبه‌بندی پلیرها", callback_data="ranking"),
         InlineKeyboardButton("👮🏻‍♂️ تست ورودی کلن", callback_data="test")],
        [InlineKeyboardButton("📆 برنامه‌ریزی کلن وار", callback_data="war")],
        [InlineKeyboardButton("📸 گالری افتخارات", callback_data="gallery"),
         InlineKeyboardButton("🧑‍💻 ارتباط با پشتیبانی", callback_data="support")],
        [InlineKeyboardButton("📜 قوانین کلن", callback_data="rules"),
         InlineKeyboardButton("🧗🏻‍♂️ تمرین تیمی", callback_data="training")],
        [InlineKeyboardButton("❓ راهنما و سوالات", callback_data="help"),
         InlineKeyboardButton("🗳 ارسال نظر ناشناس", callback_data="anonymous")]
    ])

def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ برگشت", callback_data="back")]])

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    if check_membership(update, context):
        context.bot.send_message(chat_id=user.id, text=START_MSG_MAIN, reply_markup=main_menu_keyboard())
    else:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("عضو شدن 🔗", url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton("بررسی عضویت 🔄", callback_data="verify")]
        ])
        context.bot.send_message(chat_id=user.id, text=START_MSG_NEW, reply_markup=keyboard)

START_MSG_NEW = """🎮 خوش اومدی به ربات رسمی کلن IR.P.F!

برای دسترسی به امکانات ربات، ابتدا باید عضو کانال رسمی ما بشی 📢

لطفاً روی دکمه «عضو شدن 🔗» بزن و بعد از عضویت، گزینه «بررسی عضویت 🔄» رو انتخاب کن👇
"""

START_MSG_VERIFIED = """✅ عضویت شما با موفقیت تأیید شد!

🎉 Welcome, soldier! You’re now verified as a member of our official channel.
"""

WELCOME_PRIVATE = """🎉 عضویت شما در کانال رسمی کلن IR.P.F با موفقیت ثبت شد!
فرزند پارسی، به جمع ما خوش اومدی 🌟
📌 لطفاً همین حالا وارد ربات شو و بخش «📜 قوانین کلن» رو مطالعه کن.
"""

START_MSG_MAIN = """🎮 به ربات رسمی کلن  IR.P.F خوش اومدی!

اینجا می‌تونی:
• رتبه‌بندی بازیکنان کلن رو ببینی 🏆  
• تست برای ورود به کلن بدی👮🏻‍♂️
• برنامه کلن وار رو دنبال کنی 📆  
• با ادمین‌ها در تماس باشی 🧑‍💻  
• افتخارات ثبت‌شده کلن رو ببینی 📸  
• قوانین و راهنماها رو بخونی 📜  
• تمرین تیمی رو انتخاب کنی 🧗🏻‍♂️
• نظرت رو ناشناس بفرستی 🗳
"""

NOT_MEMBER_MSG = """❌ شما هنوز عضو کانال رسمی ما نیستید.

📢 لطفاً ابتدا در کانال عضو شوید تا بتوانید از امکانات ربات استفاده کنید.
"""

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    user = query.from_user

    if data == "verify":
        if check_membership(update, context):
            context.bot.send_message(chat_id=user.id, text=START_MSG_VERIFIED, reply_markup=main_menu_keyboard())
            context.bot.send_message(chat_id=user.id, text=WELCOME_PRIVATE)
        else:
            context.bot.send_message(chat_id=user.id, text=NOT_MEMBER_MSG)

    elif data == "back":
        query.edit_message_text(text=START_MSG_MAIN, reply_markup=main_menu_keyboard())

    elif data == "ranking":
        msg = "🏆 جدول رتبه‌بندی بازیکنان کلن IR.P.F\n\nAlis: 1550 pt\nMms:250 pt"
        query.edit_message_text(text=msg, reply_markup=back_button())

    elif data == "test":
        query.edit_message_text(text="درخواست شما ثبت شد.", reply_markup=back_button())
        context.bot.send_message(chat_id=f"@{ADMIN_USERNAME}", text=f"@{user.username} درخواست تست کلن داد.")

    elif data == "war":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ شرکت می‌کنم", callback_data="war_yes"),
             InlineKeyboardButton("❌ شرکت نمی‌کنم", callback_data="war_no")],
            [InlineKeyboardButton("⬅️ برگشت", callback_data="back")]
        ])
        msg = "📆 برنامه کلن وار این هفته:\n\n🕹 چهارشنبه ۲۲:۰۰ - CLAN-X\n🕹 جمعه ۲۱:۳۰ - Elite Warriors"
        query.edit_message_text(text=msg, reply_markup=keyboard)

    elif data == "war_yes":
        context.bot.send_message(chat_id=f"@{ADMIN_USERNAME}", text=f"@{user.username} شرکت در کلن وار را تأیید کرد.")
        query.edit_message_text(text="✅ ثبت شد: شما در وار شرکت می‌کنید.", reply_markup=back_button())

    elif data == "gallery":
        msg = "📸 گالری افتخارات کلن IR.P.F\n🌟 بهترین حمله هفته\n🥇 MVP کلن وار"
        query.edit_message_text(text=msg, reply_markup=back_button())

    elif data == "support":
        msg = f"🧑‍💻 پشتیبانی رسمی کلن IR.P.F\n\n🆔 @{ADMIN_USERNAME}"
        query.edit_message_text(text=msg, reply_markup=back_button())

    elif data == "rules":
        msg = "📜 قوانین رسمی کلن IR.P.F\n\n1. احترام متقابل..."
        query.edit_message_text(text=msg, reply_markup=back_button())

    elif data == "training":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("شنبه", callback_data="train_sat"),
             InlineKeyboardButton("یکشنبه", callback_data="train_sun")],
            [InlineKeyboardButton("سه‌شنبه", callback_data="train_tue"),
             InlineKeyboardButton("چهارشنبه", callback_data="train_wed")],
            [InlineKeyboardButton("⬅️ برگشت", callback_data="back")]
        ])
        msg = "🧗🏻‍♂️ تمرین تیمی این هفته:\nشنبه، یکشنبه، سه‌شنبه و چهارشنبه."
        query.edit_message_text(text=msg, reply_markup=keyboard)

    elif data.startswith("train_"):
        day = data.split("_")[1]
        days = {"sat": "شنبه", "sun": "یکشنبه", "tue": "سه‌شنبه", "wed": "چهارشنبه"}
        context.bot.send_message(chat_id=f"@{ADMIN_USERNAME}", text=f"@{user.username} تمرین روز {days[day]} را انتخاب کرد.")
        query.edit_message_text(text=f"✅ ثبت شد: تمرین روز {days[day]}.", reply_markup=back_button())

    elif data == "help":
        msg = "❓ راهنمای استفاده از ربات..."
        query.edit_message_text(text=msg, reply_markup=back_button())

    elif data == "anonymous":
        user_states[user.id] = "anonymous"
        context.bot.send_message(chat_id=user.id, text="🗳 لطفاً متن مورد نظر خود را ارسال کنید:")

def handle_message(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.id in user_states and user_states[user.id] == "anonymous":
        msg = update.message.text
        context.bot.send_message(chat_id=f"@{ADMIN_USERNAME}", text=f"پیام ناشناس از @{user.username}: {msg}")
        update.message.reply_text("✅ پیام شما ناشناس ثبت شد.")
        user_states.pop(user.id, None)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
