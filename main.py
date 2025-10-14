import os
import telebot
from functions import getTopMarketNews, find_upcoming_earnings
from telebot import types
from dotenv import load_dotenv

# === Load token ===
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telebot.TeleBot(TOKEN)
if not TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN in .env")

# Get top market news
newsArray = getTopMarketNews()
newsMessage = f"<b>Top Market News By CNBC</b>\n"
for x in newsArray:
    newsMessage += f'<a href="{x["url"]}">{x["headline"]}</a>\n\n'

earningsMessage = find_upcoming_earnings()

bot.send_message(CHAT_ID, newsMessage, parse_mode="HTML", disable_web_page_preview=True)
bot.send_message(CHAT_ID, earningsMessage, parse_mode="HTML", disable_web_page_preview=True)
