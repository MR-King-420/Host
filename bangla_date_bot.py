import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from datetime import datetime
from dateutil import parser

# বাংলা মাস ও ঋতুর ম্যাপিং
BANGLA_MONTHS = {
    1: ("বৈশাখ", "গ্রীষ্ম"),
    2: ("জ্যৈষ্ঠ", "গ্রীষ্ম"),
    3: ("আষাঢ়", "বর্ষা"),
    4: ("শ্রাবণ", "বর্ষা"),
    5: ("ভাদ্র", "শরৎ"),
    6: ("আশ্বিন", "শরৎ"),
    7: ("কার্তিক", "হেমন্ত"),
    8: ("অগ্রহায়ণ", "হেমন্ত"),
    9: ("পৌষ", "শীত"),
    10: ("মাঘ", "শীত"),
    11: ("ফাল্গুন", "বসন্ত"),
    12: ("চৈত্র", "বসন্ত"),
}

# বিশেষ দিনের ডেটা
SPECIAL_DAYS = {
    (4, 14): "পহেলা বৈশাখ",
    (12, 16): "বিজয় দিবস",
    (3, 26): "স্বাধীনতা দিবস",
}

# বাংলা তারিখ কনভার্টার (সরলীকৃত)
def english_to_bangla_date(english_date):
    try:
        date_obj = parser.parse(english_date)
        day = date_obj.day
        month = date_obj.month
        year = date_obj.year - 593  # ইংরেজি থেকে বাংলা সন (আনুমানিক)
        
        bangla_month, season = BANGLA_MONTHS.get(month, ("অজানা", ""))
        special_day = SPECIAL_DAYS.get((month, day), "")
        
        return f"{day} {bangla_month}, {year} ({season})", special_day
    except Exception as e:
        return None, None

# টেলিগ্রাম কমান্ড হ্যান্ডলার
def date_command(update: Update, context: CallbackContext):
    user_input = " ".join(context.args)
    if not user_input:
        update.message.reply_text("⚠️ ব্যবহার: /date <YYYY-MM-DD> (যেমন: /date 2024-04-14)")
        return
    
    bangla_date, special_day = english_to_bangla_date(user_input)
    if bangla_date:
        response = f"📅 ইংরেজি: {user_input}\n"
        response += f"🇧🇩 বাংলা: {bangla_date}\n"
        if special_day:
            response += f"🎉 বিশেষ দিন: **{special_day}**"
        update.message.reply_text(response)
    else:
        update.message.reply_text("❌ তারিখ প্যার্স করতে সমস্যা! সঠিক ফরম্যাট ব্যবহার করুন (YYYY-MM-DD)।")

def time_now(update: Update, context: CallbackContext):
    now = datetime.now()
    bangla_date, _ = english_to_bangla_date(now.strftime("%Y-%m-%d"))
    response = f"🕒 এখন সময়: {now.strftime('%I:%M %p')}\n"
    response += f"📅 আজকের তারিখ: {bangla_date}"
    update.message.reply_text(response)

# মেইন ফাংশন
def main():
    # টেলিগ্রাম বট টোকেন দিয়ে প্রতিস্থাপন করুন
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # কমান্ড হ্যান্ডলার
    dp.add_handler(CommandHandler("date", date_command, pass_args=True))
    dp.add_handler(CommandHandler("time", time_now))

    # লগিং
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
