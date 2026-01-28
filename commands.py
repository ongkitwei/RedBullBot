import html
from telebot import types
from telebot import util
from prompts import stock_analysis_prompt, earnings_summary_prompt
from keyboards import get_persistent_menu

def process_ai_response(message, bot, llm, selected_prompt):
    chat_id = message.chat.id
    stock_name = message.text
    
    remove_markup = types.ReplyKeyboardRemove()
    
    loading_msg = bot.send_message(
        chat_id, 
        f"🤖 <i>Analyzing {stock_name}...</i>", 
        parse_mode="HTML",
        reply_markup=remove_markup
    )
    
    try:
        prompt = (
            selected_prompt(stock_name)
        )
        
        response = llm.invoke(prompt)
        chunks = util.smart_split(response.content, chars_per_string=3900)

        for i, chunk in enumerate(chunks):
            safe_chunk = html.escape(chunk)
            text = f"\n\n{safe_chunk}" if len(chunks) > 1 else safe_chunk
            is_last_chunk = (i == len(chunks) - 1)
            if is_last_chunk:
                bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=get_persistent_menu())
            else:
                bot.send_message(chat_id, text, parse_mode="HTML")
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Error: {str(e)}", reply_markup=get_persistent_menu())
    
    finally:
        bot.delete_message(chat_id, loading_msg.message_id)