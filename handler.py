from django import dispatch
import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters

token = '5221097095:AAGJaWVAU0i0eWf7FHI7ioGRzgB9pHlVdqs'
id = '5160184450'

bot = telegram.Bot(token)

# updater
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
# 봇
updater.start_polling()

def handler(update, context):
    user_text = update.message.text
    if user_text == '안녕':
        bot.send_message(chat_id=id, text='안녕하세요')
    elif user_text == 'Hi':
        bot.send_message(chat_id=id, text='Hello!')

echo_handler = MessageHandler(Filters.text, handler)
dispatcher.add_handler(echo_handler)
    