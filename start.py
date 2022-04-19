import telegram

token = '5221097095:AAGJaWVAU0i0eWf7FHI7ioGRzgB9pHlVdqs'
id = '5160184450'

bot = telegram.Bot(token)
bot.sendMessage(chat_id=id, text='테스트 코드')