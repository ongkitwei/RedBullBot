from telebot import types

def get_persistent_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, is_persistent=True)
    btn_ai = types.KeyboardButton("🤖 AI Stock Analysis")
    btn_earnings = types.KeyboardButton("📊 Earnings Summary")
    # btn_iv_calculator = types.KeyboardButton("🔢 Intrinsic Value Calculator")
    # btn_earnings_date = types.KeyboardButton("📅 Earnings Date")
    markup.add(btn_ai, btn_earnings)
    return markup