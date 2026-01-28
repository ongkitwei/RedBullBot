import os
import telebot
import html
from telebot import types
from telebot import util
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from functions import getTopMarketNews, find_upcoming_earnings
from clean_ai_response import escape_for_html
from prompts import stock_analysis_prompt, earnings_summary_prompt
from commands import process_ai_response
from keyboards import get_persistent_menu

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

bot = telebot.TeleBot(TOKEN)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7
)

@bot.message_handler(commands=['start', 'menu'])
def setup_menu(message):
    bot.send_message(
        message.chat.id, 
        "✅ <b>Bot is ready!</b>\n\n• Tap the text box to chat with friends.\n• Minimize the keyboard to see these buttons.", 
        reply_markup=get_persistent_menu(),
        parse_mode="HTML"
    )

@bot.message_handler(func=lambda message: message.text in ["🤖 AI Stock Analysis", "📊 Earnings Summary"])
def handle_menu_click(message):
    chat_id = message.chat.id
    force_reply = types.ForceReply(selective=True)
    
    if message.text == "🤖 AI Stock Analysis":
        msg = bot.send_message(chat_id, "👇 <b>Type the Stock Symbol for Analysis:</b>", 
                               parse_mode="HTML", reply_markup=force_reply)
        bot.register_next_step_handler(msg, process_ai_response, bot, llm, stock_analysis_prompt)
        
    elif message.text == "📊 Earnings Summary":
        # msg = bot.send_message(chat_id, "👇 <b>Type the Stock Symbol for Earnings:</b>", 
        #                        parse_mode="HTML", reply_markup=force_reply)
        # bot.register_next_step_handler(msg, process_ai_response, bot, llm, earnings_summary_prompt)
        bot.send_message(chat_id, "Feature coming soon 😛", parse_mode="HTML", reply_markup=get_persistent_menu())

    elif message.text == "🔢 Intrinsic Value Calculator":
        # msg = bot.send_message(chat_id, "👇 <b>Type the Stock Symbol for Earnings:</b>", 
        #                        parse_mode="HTML", reply_markup=force_reply)
        # bot.register_next_step_handler(msg, process_ai_response, bot, llm, earnings_summary_prompt)
        bot.send_message(chat_id, "Feature coming soon 😛", parse_mode="HTML", reply_markup=get_persistent_menu())

    elif "Earnings Date" in message.text:
        # msg = bot.send_message(chat_id, "👇 <b>Type the Stock Symbol for Earnings:</b>", 
        #                        parse_mode="HTML", reply_markup=force_reply)
        # bot.register_next_step_handler(msg, process_ai_response, bot, llm, earnings_summary_prompt)
        bot.send_message(chat_id, "Feature coming soon 😛", parse_mode="HTML", reply_markup=get_persistent_menu())

bot.delete_webhook(drop_pending_updates=True)
print("Bot is running...")
bot.infinity_polling()