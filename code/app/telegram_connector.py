import telegram
from emoji import emojize
from app import app

def botSendMessage(msg):
    bot = telegram.Bot(token=app.config['TOKEN_TELEGRAM'])
    chat_id=app.config['TELEGRAM_CHATID']
    bot.send_message(chat_id=chat_id, text=emojize(msg))
